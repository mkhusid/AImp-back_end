import jwt

from .validators import Min_pass_length, Mail_validator, EmailException, PassException
from django.http import HttpResponse, JsonResponse, HttpRequest
import json
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import SUser,Audio
from django.contrib import auth

class Auth(object):
    token=""



def main(request):
    return HttpResponse("")



def get_token(payload):
    Auth.token = jwt.encode(payload, 'secret', algorithm='HS256')
    return Auth.token

@csrf_exempt
def signup_view(request):
    val_email= Mail_validator()
    pass_val = Min_pass_length()
    body = json.loads(str(request.body.decode('utf-8')))
    username = body.get("username")
    email = body.get("email")
    password = body.get("pass")
    try:
        val_email.__call__(email)
        pass_val.validate(password)
        signup_body = {"username": username, "emai": email, "pass": password, }
        SUser.objects.create_user( username, email, password)
    except EmailException as ex:
        return JsonResponse("Wrong email format.".format(ex),safe=False)
    except PassException as pe:
        return JsonResponse("Password is to short.".format(pe), safe=False)
    else:
        return JsonResponse("You were successfully registered as %s"%signup_body['username'], safe=False)


@csrf_exempt
def signin_view(request):
    if request.method == 'POST':
        body = json.loads(str(request.body.decode('utf-8')))
        username = body.get("username")
        email = body.get("email")
        password = body.get("pass")
        user_auth = auth.authenticate(username=username, password=password)
        signin_body = {"username": username, "email": email, "pass": password, }
        if user_auth and user_auth.is_active:
            auth.login(request, user_auth)
            get_token(signin_body)
            #request.META['HTTP_AUTHORIZATION'] = tk
            return JsonResponse(str(Auth.token), safe=False)
        else:
            return JsonResponse("Wrong login or password.", safe=False)


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        body = json.loads(str(request.body.decode('utf-8')))
        if str(Auth.token) == str(request.META['HTTP_AUTHORIZATION']) :
            a_pk = jwt.decode(Auth.token, 'secret')['username']
            title = body.get("title")
            author = SUser.objects.get(username=a_pk)
            url = body.get("url")
            track = Audio(title=title, author=author, url=url)
            track.save()
            return JsonResponse(str(a_pk), safe=False)
        else:
            return JsonResponse("You have no permissions!", safe=False)
