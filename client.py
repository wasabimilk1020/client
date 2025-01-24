from cProfile import run
from serial import win32
import socketio
import datetime
import threading
import time
from mainloop import mainLoop
import button_schedule
import queue

# 마지막으로 pong을 받은 시간
last_pong_time = None
PONG_TIMEOUT = 4  # 초 (pong 응답 대기 시간)

character_list={"데스크": "핸들값asdfasdf", "꿀당콩": "핸들값sfsda", "이해의시계": "gosemfsf", "출발의계산": "xcvxcv", "현란한에틴": "qweqwe", "기가바이트": "lkljkl", "라이젠": "bvnvbn", "라라랜드": "핸들값sfsda", "이해의수건": "gosemfsf", "합의계산": "xcvxcv"}

# 작업 큐 생성
task_queue = queue.Queue()

# 작업 처리 스레드 함수
def process_tasks():
  while True:
    try:
      # 큐에서 작업 가져오기
      task = task_queue.get(timeout=10)
      if task is None:
        break  # None이 들어오면 스레드 종료
      print("클라이언트 메인루프 시작")
      # 작업 실행
      func, args = task
      func(*args)
    except queue.Empty:
      continue  # 작업이 없으면 다시 대기
    except Exception as e:
      print(f"Error processing task: {e}")
    

# 작업 처리 스레드 시작
worker_thread = threading.Thread(target=process_tasks, daemon=True)
worker_thread.start()

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

button_mapping={
  "모닝":button_schedule.dungeon,
  "우편":button_schedule.postBox,
  "격전의섬":button_schedule.dungeon,
  "파괴된성채":button_schedule.dungeon,
  "크루마탑":button_schedule.dungeon,
  "안타라스":button_schedule.dungeon,
  "시즌패스":button_schedule.dungeon,

}

@sio.event
def button_schedule(data):
#emit_data={"버튼이름":[데이터],"character_list":[{"아이디1":핸들 값1,"아이디2":핸들 값2}]}
  for idx, (key, value) in enumerate(data.items()):
    if idx==0:
      button_name=key
      func_data=value
    elif idx==1:
      id_handle=value
  
  # 버튼에 해당하는 함수 가져오기
  print("버튼이름: ",button_name)
  btn_func = button_mapping[button_name]

  # mainLoop 호출을 큐에 추가
  task_queue.put((mainLoop, (sio, btn_func, func_data, id_handle, button_name)))


@sio.event
def pong(data):
    global last_pong_time
    print(f"Received pong from server: {data['message']}")
    last_pong_time = time.time()  # pong 수신 시 갱신

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




