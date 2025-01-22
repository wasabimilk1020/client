from cProfile import run
from serial import win32
import socketio

character_list={"데스크": "핸들값asdfasdf", "꿀당콩": "핸들값sfsda", "이해의시계": "gosemfsf", "출발의계산": "xcvxcv", "현란한에틴": "qweqwe", "기가바이트": "lkljkl", "라이젠": "bvnvbn", "라라랜드": "핸들값sfsda", "이해의수건": "gosemfsf", "합의계산": "xcvxcv"}

#웹소켓 통신
sio = socketio.Client()

@sio.event
def connect():
  print('connection established')   

@sio.event
def disconnet():
  print("서버와 연결 끊김")

@sio.event
def reqAccount(data):
  print(data)
  sio.emit("revAccount", character_list)
# @sio.event
# def pong():

sio.connect('http://127.0.0.1:4000?computer_id=PC01')


sio.wait()




