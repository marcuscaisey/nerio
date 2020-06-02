import json

from django.db.models import F
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import URLCreationForm, URLRenamingForm
from .models import URL


def home(request):
    """
    GET
        Render the home template with an empty url creation form and either the
        currently logged in user's urls or the urls stored in the current
        session.

    POST
        Process the form data from a submitted url creation form. If the form is
        valid, redirect back to the home view. If not, then process the request
        as if it was a GET, replacing the empty url creation form with the
        current invalid form.
    """
    if request.method == "POST":
        form = URLCreationForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                url = form.save(commit=False)
                url.created_by = request.user
                url.save()
            else:
                url = form.save()
                session_urls = request.session.setdefault("urls", [])
                session_urls.append(url.id)
                request.session.modified = True

            return redirect("core:home")
    else:
        form = URLCreationForm()

    if request.user.is_authenticated:
        urls = request.user.urls
    else:
        session_urls = request.session.get("urls", [])
        urls = URL.objects.filter(pk__in=session_urls)

    urls = urls.order_by("-created_at")

    return render(request, "core/home.html", {"form": form, "urls": urls})


def forward_url(request, name):
    """
    Forward the user to the target of the url with the given name and increment
    its visit count by 1. Return a 404 if a url with the given name doesn't
    exist.
    """
    url = get_object_or_404(URL, name=name)
    url.visits = F("visits") + 1
    url.save()
    return redirect(url.target)


def modify(request, pk):
    """
    Endpoint to allow renaming and deleting of a user's urls. Valid methods are
    PATCH and DELETE.

    For all errors apart from 405 Method Not Allowed, the response will be as
    follows:
    {
        "error": "message describing error"
    }

    For both PATCH and DELETE methods, return a 404 if the requested url doesn't
    exist and 403 if the requesting user doesn't own the requested url.

    PATCH
        Rename a user's url with the following request body:
        {
            "name": "new name for url"
        }

        If successful, the response will be as follows:
        {
            "name" "new name for url",
            "url": "new shortened url",
        }

        If an error occurs when saving the new name, the error message will be
        returned instead.

    DELETE
        Delete a user's url. There is no request body required and no body in
        the response if the deletion is successful.
    """
    allowed_methods = ("PATCH", "DELETE")
    if request.method not in allowed_methods:
        return HttpResponseNotAllowed(allowed_methods)

    try:
        url = URL.objects.get(pk=pk)
    except URL.DoesNotExist:
        return JsonResponse({"error": "This URL doesn't exist."}, status=404)

    if (request.user.is_authenticated and request.user != url.created_by) or (
        not request.user.is_authenticated
        and url.pk not in request.session.get("urls", [])
    ):
        return JsonResponse(
            {"error": "You don't have permission to modify this URL."}, status=403
        )

    if request.method == "PATCH":
        data = json.loads(request.body)
        form = URLRenamingForm(data, instance=url)
        if form.is_valid():
            url = form.save()
            return JsonResponse(
                {"name": url.name, "url": url.get_absolute_url()}, status=200
            )
        else:
            return JsonResponse({"error": form.errors["name"][0]}, status=200)

    elif request.method == "DELETE":
        url.delete()
        return JsonResponse({}, status=200)
