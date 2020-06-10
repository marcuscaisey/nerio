import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import F
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import URLCreationForm, URLRenamingForm
from .models import URL


def home(request):
    """
    GET
        Display the URLCreationForm and a list of urls.

        Context:
            - form: An unbound URLCreationForm instance.
            - page: A Page from the url Paginator.

        Parameters:
            - page: The page number to display.

    POST
        Process the form data from a submitted URLCreationForm.

        If the data is valid:
            - Create a URL, either storing the ID in the user's session or
              assigning the URL to them depending on whether they are logged in
              or not.
            - Redirect to the home view.
            - Add a success message.

        If not, redisplay the form with errors.
    """
    if request.method == "POST":
        form = URLCreationForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)

            if request.user.is_authenticated:
                url.created_by = request.user

            try:
                url.save()
            except IntegrityError:
                form = URLCreationForm(request.POST)
            else:
                if not request.user.is_authenticated:
                    session_urls = request.session.setdefault("urls", [])
                    session_urls.append(url.id)
                    request.session.modified = True

                messages.success(request, "URL has been shortened.")

                return redirect("core:home")
    else:
        form = URLCreationForm()

    if request.user.is_authenticated:
        urls = request.user.urls
    else:
        session_urls = request.session.get("urls", [])
        urls = URL.objects.filter(pk__in=session_urls)

    urls = urls.exclude(is_active=False).order_by("-created_at")

    paginator = Paginator(urls, 5)
    page = paginator.get_page(request.GET.get("page"))

    return render(request, "core/home.html", {"form": form, "page": page})


def forward(request, name):
    """
    Forward the user to the target of the url with the given name and increment
    its visit count by 1. Return a 404 if a url with the given name doesn't
    exist.
    """
    url = get_object_or_404(URL, name_lower=name.lower())
    url.visits = F("visits") + 1
    url.save()
    return redirect(url.target)


def modify(request, pk):
    """
    Endpoint to allow renaming and deleting of a user's urls. Valid methods are
    PATCH and DELETE. A 405 Method Not Allowed will be returned if an invalid
    method is used. All other responses will be in JSON.

    PATCH
        Rename a user's url.

        Request:
            {
                "name": "new name for url"
            }

        Response:
            Success:
                {
                    "name" "new name for url",
                    "url": "new shortened url in absolute form",
                }

            Error:
                {
                    "error": "message describing error"
                }

    DELETE
        Delete a user's url.

        Request:
            {}

        Response:
            Success:
                {}
                As well as the response, a message will be added.

            Error:
                {
                    "error": "message describing error"
                }
    """
    allowed_methods = ("PATCH", "DELETE")
    if request.method not in allowed_methods:
        return HttpResponseNotAllowed(allowed_methods)

    try:
        url = URL.objects.get(pk=pk)
    except URL.DoesNotExist:
        return JsonResponse({"error": "This URL doesn't exist."}, status=404)

    if (request.user.is_authenticated and request.user != url.created_by) or (
        not request.user.is_authenticated and url.pk not in request.session.get("urls", [])
    ):
        return JsonResponse({"error": "You don't have permission to modify this URL."}, status=403)

    if request.method == "PATCH":
        data = json.loads(request.body)
        form = URLRenamingForm(data, instance=url)
        if form.is_valid():
            try:
                url = form.save()
            except IntegrityError:
                form = URLRenamingForm(data)
                return JsonResponse({"error": form.errors["name"][0]}, status=200)

            root_url = f"{request.scheme}://{request.get_host()}"
            url_path = reverse("core:forward", args=(url.name,))
            return JsonResponse({"name": url.name, "url": f"{root_url}{url_path}"}, status=200)

        else:
            return JsonResponse({"error": form.errors["name"][0]}, status=200)

    elif request.method == "DELETE":
        url.is_active = False
        url.save()
        messages.success(request, "URL has been deleted.")
        return JsonResponse({}, status=200)
