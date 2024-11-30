from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from .models import UserData
from .seralizers import UserDataSerializer

@api_view(['POST', 'GET', 'DELETE'])
@csrf_exempt
def passwords(request):

    match request.method:
        #Get user data, if user doesnt exist, create a new one
        case "GET":
            data = JSONParser().parse(request)
            uid = data["uid"]
            user_data, exits = UserData.objects.get_or_create(uid=uid, defaults={"uid":uid, "passwords":{}})

            serialize = UserDataSerializer(user_data)
            return JsonResponse(serialize.data, status = 200)
        
        case "POST":
            data = request.data #JsonParser doesnt work when the request is from js for some reason

            try:
                uid = data["uid"]
                user_data, exits = UserData.objects.get_or_create(uid=uid, defaults={"uid":uid, "passwords":{}})                
                site = data["site"]
                #Password is sent from the client pre encrypted
                salt = data["salt"]
                iv = data["iv"]
                cipher = data["cipher"]

                user_data.passwords[site] = {
                    "salt":salt,
                    "iv":iv,
                    "cipher": cipher
                }

                user_data.save()

                serialize = UserDataSerializer(user_data)
                return JsonResponse({'sucess':'entry added'}, status = 201)
            except:
                return JsonResponse({'error':'bad request, request must contain \'uid\',\'site\',\'salt\',\'iv\',\'cipher\''}, status=400)
        
        case "DELETE":
            data = request.data
            try:
                uid = data["uid"]
                site = data["site"]

                userExists = UserData.objects.filter(uid=uid).exists
                
                if not userExists:
                    return JsonResponse({'error':'user doesnt exist'},status=404)
                
                user_data = UserData.objects.get(uid=uid)
                del user_data.passwords[site]
                user_data.save()
            except:
                return JsonResponse({'error':'bad request, request must contain \'uid\',\'site\''}, status=400)

            return JsonResponse({'sucess':'entry deleted'}, status = 204)

        case _:
            return JsonResponse({'error':'doesnt exist'}, status = 404)
