# -*- coding: utf-8 -*-
from flask import request, jsonify

from init import db, app
from models import User, Message, Attachment, Invitation, Chat
from datetime import datetime


@app.route('/registration', methods=['POST'])
def registration():
    username = str(request.form['username'])
    email = str(request.form['email'])
    password = str(request.form['password'])
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return 'Created', 201


@app.route('/users/<user_id>', methods=['GET', 'PUT'])
def method_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'GET':
        data = {'username': user.username, 'email': user.email, 'last_seen': user.last_seen}
        return jsonify(data)
    else:
        username = str(request.form['username'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        user.username = username
        user.email = email
        user.set_password(password)
        db.session.commit()
        return 'Updated', 200


@app.route('/chat', methods=['POST'])
def create_chat():
    name = str(request.form['name'])
    chat = Chat(name=name)
    db.session.add(chat)
    db.session.commit()
    return 'Created', 201


@app.route('/chats/<chat_id>', methods=['GET', 'PUT', 'DELETE'])
def method_chat(chat_id):
    chat = Chat.query.get(chat_id)
    if request.method == 'GET':
        data = {'name': chat.name, 'image': chat.image}
        return jsonify(data)
    elif request.method == 'PUT':
        name = str(request.form['name'])
        chat.name = name
        db.session.commit()
        return 'Updated', 200
    else:
        db.session.delete(chat)
        db.session.commit()
        return 'Deleted', 204


@app.route('/invitation', methods=['POST'])
def create_invitation():
    user_id = str(request.form['user_id'])
    chat_id = str(request.form['chat_id'])
    chat = Chat.query.get(chat_id)
    user = User.query.get(user_id)
    invitation = Invitation()
    invitation.user = user
    invitation.chat = chat
    db.session.add(invitation)
    db.session.commit()
    return 'Created', 201


@app.route('/accept_the_invitation/<invitation_id>')
def accept_the_invitation(invitation_id):
    invitation = Invitation.query.get(int(invitation_id))
    invitation.user.chats.append(invitation.chat)
    db.session.delete(invitation)
    db.session.commit()
    return 'Ok', 200


@app.route('/decline_the_invitation/<invitation_id>')
def decline_the_invitation(invitation_id):
    invitation = Invitation.query.get(invitation_id)
    db.session.delete(invitation)
    db.session.commit()
    return 'Deleted', 200


@app.route('/users/<user_id>/chats')
def user_chat(user_id):
    user = User.query.get(user_id)
    data = [{'chat_id': chat.id, 'chat_name': chat.name, 'chat_image': chat.image} for chat in user.chats]
    return jsonify(data)


@app.route('/chats/<chat_id>/users')
def chat_user(chat_id):
    chat = Chat.query.get(chat_id)
    data = [{'user_id': user.id, 'username': user.username} for user in chat.users]
    return jsonify(data)


@app.route('/chats/<chat_id>/message', methods=['POST'])
def write_message(chat_id):
    user_id = str(request.form['user_id'])
    chat = Chat.query.get(chat_id)
    user = User.query.get(user_id)
    body = str(request.form['body'])
    message = Message(body=body)
    message.author = user
    message.chat = chat
    message.timestamp = datetime.now()
    db.session.add(message)
    db.session.commit()
    return 'Created', 201


@app.route('/messages/<message_id>', methods=['GET', 'PUT', 'DELETE'])
def method_message(message_id):
    message = Message.query.get(message_id)
    if request.method == 'GET':
        data = {'author': {'username': message.author.username}, 'body': message.body, 'timestamp': message.timestamp}
        return jsonify(data)
    elif request.method == 'PUT':
        body = str(request.form['body'])
        message.body = body
        db.session.commit()
        return 'Updated', 200
    else:
        db.session.delete(message)
        db.session.commit()
        return 'Deleted', 204


@app.route('/chats/<chat_id>/messages')
def chat_messages(chat_id):
    chat = Chat.query.get(chat_id)
    data = [{'id': message.id, 'author': {'username': message.author.username}, 'body': message.body, 'timestamp': message.timestamp}
            for message in chat.posts]
    return jsonify(data)
