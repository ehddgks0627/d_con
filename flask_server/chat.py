#!/usr/bin/env python
import time
import random
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect
from pymysql import connect

# DB
async_mode = None

server_domain = "0.0.0.0"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'this isssssssssssss secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
conn = connect(host='layer7.kr', port=3306, user='em', passwd='fuckkk', db='d_con', charset ='utf8')
conn.autocommit(1)
cur = conn.cursor()
background_count = 7

@app.route('/')
@app.route('/list/')
def list():
    try:
        return render_template('chat_list.html',random=random.randint(1,background_count));
    except:
        return "error"

@app.route('/make/')
def make():
    try:
        return render_template('chat_make.html',random=random.randint(1,background_count))
    except:
        return "error"

@app.route('/chat/', methods=['POST'])
def chat():
    try:
        conn = connect(host='layer7.kr', port=3306, user='em', passwd='fuckkk', db='d_con', charset ='utf8')
        cur = conn.cursor()
        cur.execute("SELECT name FROM `room_list` WHERE `key`=%s"%(request.form['login_key']))
        return render_template('chat_chat.html', login_key=request.form['login_key'],login_name=cur.fetchall()[0][0],random=random.randint(1,background_count))
    except:
        return "error"

@socketio.on('create', namespace='/chat_base')
def create(message):
    try:
        if message['room_name'] != "":
            conn.commit()
            cur.execute("INSERT INTO `room_list` (`name`) VALUES ('%s')"%(message['room_name']))
            conn.commit()
            cur.execute("CREATE TABLE `room_%s` (`message` VARCHAR(4096) NOT NULL, `nick` VARCHAR(128) NOT NULL)ENGINE=InnoDB"%(cur.lastrowid))
            conn.commit()
            emit('success', {'url': '/list/'})
        else:
            emit('failure', {'data': 'room_name is empty'})#delete
    except:
        pass

@socketio.on('get_message', namespace='/chat_base')
def get(message):
    try:
        if not 'count' in session:
            session['count'] = 0
        cur.execute("SELECT * FROM `room_%s`"%(message['room_key']))
        datas = cur.fetchall()
        datas = datas[session['count']:]
        for data in datas:
            session['count'] += 1
            emit('write_message', {'data': '%s'%(str(data[0])),'nick': '%s'%(str(data[1]))})
    except:
        print("error")

@socketio.on('leave', namespace='/chat_base')
def leave(message):
    try:
        conn.commit()
        cur.execute("DROP TABLE `room_%s`"%(message['leave_key']))
        conn.commit()
        cur.execute("DELETE FROM `room_list` WHERE `key`='%s'"%(message['leave_key']))
        conn.commit()
        emit('move', {'location': '/list'})
    except:
        pass

@socketio.on('send_message', namespace='/chat_base')
def send_room_message(message):
    try:
        cur.execute("INSERT INTO `room_%s` VALUES ('%s','%s')"%(message['send_key'],message['send_msg'],message['send_nick']))
        conn.commit()
    except:
        pass

@socketio.on('room_list', namespace='/chat_base')
def get_room_list():
    try:
        conn = connect(host='layer7.kr', port=3306, user='em', passwd='fuckkk', db='d_con', charset ='utf8')
        cur = conn.cursor()
        conn.commit()
        cur = conn.cursor()
        cur.execute("SELECT * FROM `room_list`")
        rows = cur.fetchall()
        for row in rows:
            emit('write_room_list', {'key': row[0], 'name': row[1]})
    except:
        pass

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, host=server_domain)
