from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from main.models import Voting, VotingOption, Vote
from django import forms
from main.forms.forms import VotingForm

def voting(request, voting_id):
    voting = get_object_or_404(Voting, id=voting_id)
    context = {
        "voting": voting,
    }

    if request.method == "POST":
        form = VotingForm(request.POST, voting=voting)
        context['form'] = form
        if form.is_valid():
            option = form.cleaned_data['option']
            Vote.objects.create(user=request.user, option=option)

    else:
        form = VotingForm(voting=voting)
        context['form'] = form
    return render(request, "voting.html", context)
