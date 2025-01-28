from cProfile import run
from serial import win32
import socketio
import datetime
import threading
import time
from mainloop import mainLoop
import button_func
import queue
import hashlib
import base64
import get_account

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
  character_list=get_account.get_account_list(sio)
  sio.emit("revAccount", character_list)

button_mapping={
  "status_check_button":button_func.statusChk,  
  "사냥":button_func.normalHunting,
  "격전의섬":button_func.dungeon,
  "파괴된성채":button_func.dungeon,
  "크루마탑":button_func.dungeon,
  "안타라스":button_func.dungeon,
  "상아탑":button_func.dungeon,
  "이벤트던전":button_func.dungeon,
  "모닝":button_func.morning,
  "우편":button_func.postBox,
  "시즌패스":button_func.seasonpass,
  "아이템분해":button_func.decomposeItem,
  "스킬북분해":button_func.decomposeBook,
  "아이템삭제":button_func.itemDelete,
  "일괄사용":button_func.useItem,
  "사망체크":button_func.deathChk,
  "신탁서":button_func.paper,
  "이벤트상점":button_func.event_store,
  "아가시온":button_func.agasion,
  "모두":button_func.switch_get_item,
  "고급":button_func.switch_get_item,
  "희귀":button_func.switch_get_item,
  "40M":button_func.decomposeItem,
  "제한없음":button_func.decomposeItem,
  # "바람":button_func.decomposeItem,
  # "불":button_func.decomposeItem,
  # "물":button_func.decomposeItem,
  # "게임실행":button_func.decomposeItem,
  "다이아":button_func.showDiamond,

}

@sio.event
def button_schedule(data):
#emit_data={"버튼이름":[데이터],"character_list":{"아이디1":핸들 값1,"아이디2":핸들 값2}}
  for idx, (key, value) in enumerate(data.items()):
    if idx==0:
      button_name=key
      func_data=value
    elif idx==1:
      if  value=={}:
        id_handle=character_list
      else:
        id_handle=value
  
  # 버튼에 해당하는 함수 가져오기
  print("버튼이름: ",button_name)
  btn_func = button_mapping[button_name]

  # mainLoop 호출을 큐에 추가
  task_queue.put((mainLoop, (sio, btn_func, func_data, id_handle, button_name)))

@sio.event
def recvImage(data):
  img=data[0]
  hash_value=data[1]
  file_name=data[2]
  calculated_hash = hashlib.sha256(img.encode("utf-8")).hexdigest()
  # 해시 확인
  if hash_value==calculated_hash: 
    print("데이터 무결성 확인 완료!")
    image_data = base64.b64decode(img)
    # 파일로 저장
    with open(f"./image_files/{file_name}", "wb") as f:
      f.write(image_data)
  else:
    print("데이터가 손상되었거나 무결성 검증 실패!")

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

sio.connect('http://127.0.0.1:4000?computer_id=PC01') #클라이언트 세팅

#백그라운드 작업 시작
sio.start_background_task(send_ping)
sio.start_background_task(monitor_connection)

sio.wait()




