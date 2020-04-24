from django.conf import settings
from django.shortcuts import redirect, render

from .forms import UrlForm
from .models import Url


def home(request):
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:home")
    else:
        form = UrlForm()

    urls = Url.objects.order_by("-created_at")[:5]
    return render(
        request,
        "core/home.html",
        {"form": form, "urls": urls, "root_url": settings.ROOT_URL},
    )
