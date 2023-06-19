import re
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

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


def search(request, q):
    entries = util.list_entries()
    results = [entry for entry in entries if re.search(q, entry, re.IGNORECASE)]
    return render(request, "encyclopedia/search.html", {
        "results": results
    })


def title(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/entry.html", {"entry": entry})
    return HttpResponseRedirect(reverse("not_found"))

def not_found(request):
    return render(request, "encyclopedia/not_found.html")