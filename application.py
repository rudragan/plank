import os
import json
from functools import wraps
from time import localtime, strftime

from flask import Flask, session, render_template, request, logging, url_for, redirect, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

ENV='prod'

#from models import *

app = Flask(__name__)
socketio = SocketIO(app)
rooms = ['lounge', 'chat', 'gaming', 'coding']
channelsMessages = dict()

app.config["SESSION_TYPE"] = "filesystem"
Session(app)


if ENV == 'dev':
    app.debug=True
    engine = create_engine("postgresql://postgres:chemistry12@localhost/project2")
    db = scoped_session(sessionmaker(bind=engine))
else:
    app.debug=False
    engine = create_engine("postgres://cdoyvmjekcwbyn:59acc249ea9b6b81917c302f4bcc0e2446069481be237fa2dc90f50c7e48995e@ec2-34-192-173-173.compute-1.amazonaws.com:5432/d7d3i8n279rrqm")
    db = scoped_session(sessionmaker(bind=engine))



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return render_template('login.html',message='You need to login first.')
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=['GET','POST'])
def index():
    return render_template("login.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        password = request.form.get('password')
        username = request.form.get('username')
        confirm = request.form.get('confirm')
        #secure_password = sha256_crypt.encrypt(str(password))

        if  password == '' or username == '' or confirm == '':
            return render_template('register.html', message='Please enter required fields.')

        if not password == confirm:
            return render_template('register.html', message='Passwords do not match.')

        userrow = db.execute("SELECT * FROM users WHERE username = :username", {"username": username})
        user_exists = userrow.first()
        if not user_exists:
            db.execute("INSERT INTO users(username,password) VALUES(:username, :password)",{"username":username,"password":password})
            db.commit()
            return render_template('register.html', text = "You are now registered.")

        else:
            return render_template('register.html', message="Username is taken.")

    return render_template('register.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #print(name, password)

        if username == '' or password == '':
            return render_template('login.html', message='Please enter required fields.')
        
        
        
        usernamedata = db.execute("SELECT username FROM users WHERE username=:username ",{"username":username}).fetchone()
        passworddata = db.execute("SELECT password FROM users WHERE username=:username ",{"username":username}).fetchone()

        if usernamedata is None:
            return render_template('login.html',message= 'Username not registered.')
        else:
            for passwor_data in passworddata:
                if password == passwor_data:
                    session['username']= username
                    return redirect(url_for('chat'))
                else:
                    return render_template('login.html',message= 'Incorrect Password.')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return render_template('logout.html')

@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    username=session.get('username')
    newRoom = request.form.get('new-room')

    if request.method == 'POST':

        if newRoom in rooms:
            return render_template('chat.html',message='This channel already exists')

        rooms.append(newRoom)

    return render_template('chat.html',username=username, rooms=rooms)

@app.route('/chat', methods=['GET','POST'])
@login_required
def chat():
    username=session.get('username')
    return render_template('chat.html',username=username, rooms=rooms)


@socketio.on('message')
def message(data):
    username=session.get('username')

    #print(f"\n\n{data}\n\n")

    send({'msg':data['msg'], 'username': data['username'], 'time_stamp':
        strftime('%b-%d %I:%M%p',localtime())} , room=data['room'])

@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg':data['username'] + ' has joined the ' + data['room'] + ' room.' }, room=data['room'])

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg':data['username'] + 'has left the' + data['room'] + 'room.' }, room=data['room'])





if __name__ == '__main__':
    socketio.run(app)
