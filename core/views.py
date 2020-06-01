import json

from django.db.models import F
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import URLCreationForm, URLRenamingForm
from .models import URL


def home(request):
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
    url = get_object_or_404(URL, name=name)
    url.visits = F("visits") + 1
    url.save()
    return redirect(url.target)


def modify(request, pk):
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
