from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from main.models import Voting, VotingOption, Vote
from django import forms


def voting(request, voting_id):
    voting = get_object_or_404(Voting, id=voting_id)
    voting_options = VotingOption.objects.filter(voting_id=voting_id)
    options = []
    for i in range(len(voting_options)):
        votes = Vote.objects.filter(option_id=voting_options[i].id)
        options.append((voting_options[i], len(votes)))
    context = {
        "voting": voting,
        "voting_options" : options,
    }
    return render(request, "voting.html", context)