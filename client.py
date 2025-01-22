from cProfile import run
from serial import win32
import socketio
import datetime
import threading
import time

# 마지막으로 pong을 받은 시간
last_pong_time = None
PONG_TIMEOUT = 4  # 초 (pong 응답 대기 시간)

character_list={"데스크": "핸들값asdfasdf", "꿀당콩": "핸들값sfsda", "이해의시계": "gosemfsf", "출발의계산": "xcvxcv", "현란한에틴": "qweqwe", "기가바이트": "lkljkl", "라이젠": "bvnvbn", "라라랜드": "핸들값sfsda", "이해의수건": "gosemfsf", "합의계산": "xcvxcv"}

#웹소켓 통신
sio = socketio.Client()

@sio.event
def connect():
  print('connection established')   

@sio.event
def disconnect():
  print("서버와 연결 끊김")

@sio.event
def reqAccount(data):
  print(data)
  sio.emit("revAccount", character_list)

@sio.event
def pong(data):
    global last_pong_time
    print(f"Received pong from server: {data['message']}")
    last_pong_time = time.time()  # pong 수신 시 갱신
    print(last_pong_time)
    
def monitor_connection():
    global last_pong_time
    while True:
        if not sio.connected:
            print("서버와의 연결이 끊겼습니다. 모니터링 중단.")
            break
        if last_pong_time and time.time() - last_pong_time > PONG_TIMEOUT:
            print("서버 응답 없음, 연결 종료.")
            sio.disconnect()  # 명시적으로 연결 종료
            break
        time.sleep(1)  # 1초마다 상태 확인

def send_ping():
    while sio.connected:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sio.emit("ping", {"time": current_time})
        time.sleep(2)

sio.connect('http://127.0.0.1:4000?computer_id=PC01')

#백그라운드 작업 시작
sio.start_background_task(send_ping)
sio.start_background_task(monitor_connection)



sio.wait()




