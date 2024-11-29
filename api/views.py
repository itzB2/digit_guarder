from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST', 'GET'])
@csrf_exempt
def passwords(request):
    pass

@api_view(['POST'])
@csrf_exempt
def user_created(request):
    # data = JSONParser().parse(request)

    print("you there?")
    print(request.user)

    return JsonResponse({})