from django.shortcuts import render


def index_view(request):

    # form = First_pageForm(request.POST or None)
    # if request.method == "POST" and form.is_valid():
    #     # your calculation logic here
    #     pass
    return render(request, "login_register.html", {})