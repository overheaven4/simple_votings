from django.shortcuts import render

# Create your views here.
def new_vote_page(request):
    return render(request,"create.html",{})