from django.conf import settings
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UrlCreationForm
from .models import Url


def home(request):
    if request.method == "POST":
        form = UrlCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:home")
    else:
        form = UrlCreationForm()

    urls = Url.objects.order_by("-created_at")[:5]
    return render(
        request,
        "core/home.html",
        {"form": form, "urls": urls, "root_url": settings.ROOT_URL},
    )


def forward_url(request, name):
    url = get_object_or_404(Url, name=name)
    url.visits = F("visits") + 1
    url.save()
    return redirect(url.target)
