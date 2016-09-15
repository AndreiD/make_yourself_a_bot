#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
from watson_developer_cloud import ConversationV1
import urllib
import json
import hashlib
import pyrebase

config = {
    "apiKey": "AIzaSyAS-xxxxxxxxxxxxxxxxxx",
    "authDomain": "xxxxxxxxxxxxxxx.firebaseapp.com",
    "databaseURL": "https://xxxxxxxxxx.firebaseio.com",
    "storageBucket": "xxxxxxxxxxx.appspot.com",
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')

socketio = SocketIO(app, async_mode='eventlet')
thread = None

conversation = ConversationV1(
    username='xxxxxxxxxxxxxxxxxxxxxxxxxx',
    password='xxxxxxxxxxxxxxxxxx',
    version='2016-07-11')
workspace_id = 'xxxxxxxxxxxxxxxxxx'
context = {}
last_response = ""

response = conversation.message(workspace_id=workspace_id)
context = response["context"]


@app.route('/')
def index():
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    session['unique_conversation_id'] = str(user_ip) + "__" + str(user_agent)
    context["conversation_id"] = str(hashlib.sha256(session['unique_conversation_id'].encode('utf-8')).hexdigest())
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('communicate', namespace='/chat')
def socket_communicate(message):
    from_human_message = str(message["data"])
    global context

    bot_response = "...."
    try:
        context["conversation_id"] = str(hashlib.sha256(session['unique_conversation_id'].encode('utf-8')).hexdigest())
        response = conversation.message(workspace_id=workspace_id, message_input={'text': urllib.parse.unquote(from_human_message)}, context=context)
        context = response["context"]
        try:
            bot_response = ' '.join(response["output"]["text"])
        except Exception as ex:
            print("exception :( ", ex)

    except Exception as ex:
        print("watson exception :( ", ex)

    print("\n\nBOT SAYS: " + json.dumps(response), end="\n\n")
    
    # sometimes the fucking bot doesn't answer what it should.
    if len(bot_response) < 2:
        bot_response = "I couldn't understand that. You can type 'help' for example"

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('bot_response', {'data': bot_response, 'count': session['receive_count']})

    data = {"conversation_id": session['unique_conversation_id'], "from_human": urllib.parse.unquote(from_human_message), "from_bot": bot_response}
	
	#store data in the db...
    db.child("conversations").push(data)


@socketio.on('connect', namespace='/chat')
def socket_connect():
    print("connected...")
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/chat')
def socket_disconnect():
    global context
    context = {}
    # print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host='', port=1000, debug=True)
