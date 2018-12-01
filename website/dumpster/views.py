from django.shortcuts import render
from django.http import JsonResponse
from background_task import background

# Create your views here.
def index(request):
    return render(request, 'dumpster/index.html')


def starttasks(request):
    print("Adding hook task")
    task_check_hooks(repeat=10)
    return JsonResponse({})


@background(schedule=10)
def task_check_hooks():
    print("HOOK CHECKS HERE")
