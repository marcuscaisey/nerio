from django.conf import settings
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from .forms import URLCreationForm
from .models import URL


def home(request):
    if request.method == "POST":
        form = URLCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:home")
    else:
        form = URLCreationForm()

    urls = URL.objects.order_by("-created_at")[:5]
    return render(
        request,
        "core/home.html",
        {"form": form, "urls": urls, "root_url": settings.ROOT_URL},
    )


def forward_url(request, name):
    url = get_object_or_404(URL, name=name)
    url.visits = F("visits") + 1
    url.save()
    return redirect(url.target)
