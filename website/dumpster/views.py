from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'dumpster/index.html')


def inputuser(request):
    return render(request, 'dumpster/input_user.html')
