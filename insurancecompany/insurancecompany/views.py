from django.http import HttpResponse


def insurance_home(request):
    return HttpResponse('Welcome to the Insurance Company!')

