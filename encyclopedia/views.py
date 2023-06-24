import re
import random
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import EntryForm
from . import util


def index(request):
    q = request.GET.get("q")
    entries = util.list_entries()

    if q:
        if q in entries:
            return HttpResponseRedirect(reverse("title", args=[q]))
        return HttpResponseRedirect(reverse("search", args=[q]))
    else:
        return render(request, "encyclopedia/index.html", {"entries": entries})


def create(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            content = f"#{title}\n{content}"
            util.save_entry(title, content)

            return HttpResponseRedirect(reverse("title", args=[title]))
        else:
            return render(request, "encyclopedia/create.html", {"form": form})
    form = EntryForm()

    return render(request, "encyclopedia/create.html", {"form": form})


def search(request, q):
    entries = util.list_entries()
    results = [entry for entry in entries if re.search(q, entry, re.IGNORECASE)]
    return render(request, "encyclopedia/search.html", {"results": results})


def title(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(
            request, "encyclopedia/entry.html", {"entry": entry, "title": title}
        )
    return HttpResponseRedirect(reverse("not_found"))


def update(request, title):
    content = util.get_entry(title)

    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)

            return HttpResponseRedirect(reverse("title", args=[title]))
        else:
            return render(
                request, "encyclopedia/update.html", {"form": form, "title": title}
            )
    form = EntryForm(initial={"content": content, "title": title, "is_update": True})

    return render(request, "encyclopedia/update.html", {"form": form, "title": title})


def random_entry(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect(reverse("title", args=[entry]))


def not_found(request):
    return render(request, "encyclopedia/not_found.html")
