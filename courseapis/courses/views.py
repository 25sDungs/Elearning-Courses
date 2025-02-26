from django.http import HttpResponse

def index(request):
    return  HttpResponse("Xin chao the gioi")