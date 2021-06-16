import requests
import datetime

from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
    if request.method == 'GET':
        return render(request, 'chat/index.html')
    if request.method == 'POST':
        username, password = request.POST["username"], request.POST["password"]
        res = requests.post("http://127.0.0.1:5000/login", json={"username": username, "password": password})
        result = res.json()
        request.session["token"] = result["token"]
        request.session["id"] = result["id"]
        request.session["username"] = str(username)
        return redirect('chat')


def chat_view(request):
    username = request.session.get("username")
    token = request.session.get("token")
    uid = request.session.get("id")
    res = requests.get("http://127.0.0.1:5000/users")
    result = res.json()
    us = result["users"]
    all_user_names = [u["name"] for u in us]
    al_new = str(all_user_names).strip(']').strip('[')
    if request.method == 'GET':
        friend_name = request.session.get("friend")
        headers = {"Authorization": "JWT " + token}
        if friend_name:
            resp1 = requests.get("http://127.0.0.1:5000/messages/" + username + "/" + friend_name, headers=headers)
            res = resp1.json()
            friend_message = [m["message"] for m in res["messages"]]
            context = {"users": al_new, "username": username, "access_token": token, "friend_message": friend_message,
                       'friend_name': friend_name}
            return render(request, 'chat/chat.html', context)
        else:
            context = {"users": al_new, "username": username, "access_token": token,
                       }
            return render(request, 'chat/chat.html', context)
    if request.method == 'POST':
        message = request.POST['text']
        friend_name = request.POST['recipient']
        request.session['friend'] = friend_name
        res1 = requests.get('http://127.0.0.1:5000/user/' + friend_name)
        result1 = res1.json()
        fr_id = [u['id'] for u in result1['user']]
        friend_id = fr_id[0]
        date = datetime.datetime.utcnow()
        mesdate = f'{date.year}/{date.month}/{date.day}'
        headers = {"Authorization": "JWT " + token}
        res = requests.post('http://127.0.0.1:5000/messages', json={"text": message, "mesdate": mesdate,
                                                                    "user": uid, "for_user": friend_id},
                            headers=headers)
        context = {'user_message': message, 'friend_name': friend_name, "users": al_new, "username": username}

        return render(request, 'chat/chat.html', context)


def logout(request):
    request.session.pop('username', None)
    request.session.pop('id', None)
    request.session.pop('token', None)
    return redirect('index')


def register(request):
    if request.method == 'GET':
        return render(request, 'chat/register.html')
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        age, nickname = request.POST['age'], request.POST['nickname']
        date = datetime.datetime.utcnow()
        regdate = f'{date.year}/{date.month}/{date.day}'  #
        res = requests.post('http://127.0.0.1:5000/users', json={"name": username, "password": password,
                                                                 "nickname": nickname, "regdate": regdate, "age": age})
        context = {"username": username}
        return render(request, 'chat/new_user.html', context)
