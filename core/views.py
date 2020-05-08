from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from .forms import URLCreationForm
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
