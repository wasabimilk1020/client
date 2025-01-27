import time
import utils

def run_btn(sio, data,btn_name, character_name):
  print(f"{btn_name} 실행")
  time.sleep(1)
  return 1, None

def postBox(sio, data,btn_name, character_name):
  print(f"{btn_name} 실행")
  time.sleep(1)
  return 0, None

def dungeon(sio, data,btn_name, character_name):
  #data=[1142, 375, 10, 10, 0.0]=[x,y,xRange,yRange,delay]
  name=character_name
  if btn_name=="격전의섬":

    data=utils.caputure_image(name,387,258) #name, x, y
    sio.emit("captured_image",data)
    
    
  elif btn_name=="파괴된성채":
    print(f"{btn_name} 실행")
  elif btn_name=="크루마탑":
    print(f"{btn_name} 실행")
  elif btn_name=="안타라스":
    print(f"{btn_name} 실행")
  elif btn_name=="상아탑":
    print(f"{btn_name} 실행")
  elif btn_name=="이벤트던전":
    print(f"{btn_name} 실행")
  time.sleep(1)
  return 1, None

def decomposeItem(sio, data,btn_name, character_name):
  print(f"{btn_name} 실행")
  time.sleep(1)
  return 1, None

# #격섬 루틴
# def dungeonG(sio, data,btn_name):
#   coord=data
#   delay=data[4]
#   #격전의 섬 이동 루틴
#   keyboard("`") #던전
#   result=searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

#   result=searchImg('dungeonG.png',beforeDelay=1, afterDelay=1)
#   if(result==0):
#     return 0, "격전의 섬 클릭 실패"

#   #data 인자가 뭐가 들어오는지 확인해보고 coord가 온다면 여기서 그 인자로 층수 세팅
#   result=searchImg('dungeon_enter.png', beforeDelay=1, afterDelay=1, _region=(1200, 750, 400, 150))  #입장하기 
#   randClick(coord[0],coord[1],coord[2],coord[3],delay) 
  
#   #격섬 이동 완료 체크
#   result=searchImg('chk.png', beforeDelay=1, afterDelay=1, justChk=True, chkCnt=10,_region=(910,180,230,70))
#   if(result==0):
#     return 0, "격전의 섬 이동 실패"
  
# #여기 아래 해줄 차례
#   # --캡쳐이미지--
#   pyautogui.screenshot(f"img\capture_img\{name}.png", region=(387,258,50,30))
#   with open(f"img\capture_img\{name}.png", "rb") as f:
#     b64_string = base64.b64encode(f.read())
#     captureImg=b64_string
#   now = datetime.datetime.now()
#   nowDatetime=now.strftime('%H:%M')
#   data=[captureImg,0,name, nowDatetime] #[캡쳐, 캡쳐함수선택, 이름, 시간]
#   time.sleep(0.2)
#   sio.emit("capture_img",data)
#   # -------------

#   keyboard('6') #순간이동
  
#   return 1, None