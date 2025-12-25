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
    options_list = VotingOption.objects.filter(voting=voting)
    is_voted = False
    for option in options_list:
        vote_list = Vote.objects.filter(option=option)
        for vote in vote_list:
            if vote.user == request.user:
                is_voted = True
                context['given_vote'] = vote.option
                break
        if is_voted: break
    if is_voted:
        template_name = "voting_result.html"
        options = []
        for i in range(len(options_list)):
            votes_count = Vote.objects.filter(option=options_list[i]).count()
            options.append((options_list[i], votes_count))
        context['options_list'] = options

    else:
        template_name = "voting.html"
        if request.method == "POST":
            form = VotingForm(request.POST, voting=voting)
            if form.is_valid():
                option = form.cleaned_data['option']
                Vote.objects.create(user=request.user, option=option)
                return redirect(f'/voting/{voting_id}')

        else:
            form = VotingForm(voting=voting)
        context['form'] = form
    return render(request, template_name, context)


