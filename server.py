import time
import os
from datetime import datetime

from flask import Flask, request

app = Flask(__name__)
messages = []
users = {
    # username: password
}


@app.route("/")
def hello_view():
    return '''Надеюсь выиграю обучение! Спасибо за интенсив
              MyChat v1.00 
              Thanks for using it.
           '''


@app.route("/status")
def status_view():
    return {
        'status': True,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'users': {"users_count": len(users),
                  "names_of_users": [i for i in users.keys()]}
    }


@app.route("/messages")
def messages_view():
    print(request.args)
    after = float(request.args['after'])

    filtered_messages = []
    for message in messages:
        if message['time'] > after:
            filtered_messages.append(message)

    return {'messages': filtered_messages}


@app.route("/send", methods=['POST'])
def send_view():
    """
    Отправить сообщение всем.
    :input: {"username": str, "password": str, "text": str}
    :return: {"ok": bool}
    """
    print(request.json)
    username = request.json["username"]
    password = request.json["password"]
    text = request.json["text"]

    isAdmin = False

    if username == 'admin' and password == 'admin':
        isAdmin = True

    # функционал админки
    """/clear - очистить сообщения и консоль
       /ban - забанить юзера
    """
    if isAdmin:
        if text == '/clear':
            messages.clear()
        if text == '/ban':
            ban_name = request.json["ban_name"]
            del users[ban_name]

    if username not in users or users[username] != password:
        return {'message sended': False}

    messages.append({'username': username, 'time': time.time(), 'text': text})
    return {'message sended': True}


@app.route("/login", methods=['POST'])
def login_view():
    """
    Логин в систему.
    :input: {"username": str, "password": str}
    :return: {"ok": bool}
    """
    print(request.json)
    username = request.json["username"]
    password = request.json["password"]

    if username == 'admin' and password == 'admin':
        users[username] = password
        return {'admin': True}

    if username not in users:
        users[username] = password
        return {'logged in': True}
    elif users[username] == password:
        return {'logged in': True}
    else:
        return {'logged in': False}


if __name__ == '__main__':
    app.run()
