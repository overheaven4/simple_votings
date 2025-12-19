from django.shortcuts import render

from main.models import Voting
from main.models import Voting


def votes_page(request):
    context = {
        "items": Voting.objects.all()

    }
    return render(request,"votes.html",context)