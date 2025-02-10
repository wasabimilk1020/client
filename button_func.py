import time
import client_utils
from serial_comm import *
import re
import check_hunting
from waking_from_sleep import *
from go_to_sleep import *

#data=[1142, 375, 10, 10, 0.0]=[x,y,xRange,yRange,delay]
def statusChk(sio, data, btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name
 
  value=check_hunting.checkHunting() #value=성공 시=문자열, 실패 시=0
  if value[0]==1: #1을 return (사냥을 하지 않고 있다는 뜻)
    result=waking_from_sleep_and_deathChk(btn_name)
    if result==1: #사망 체크를 수행 했는대 chk.png가 확인 안되서 실패
      return 0, "페널티 체크 루틴 실패"
    result=normalHunting(sio, data, btn_name, character_name)
    return result
  elif value[0]==0: #capture_text_from_region 예외 발생
    return value[0], value[1]
  else:  #성공
    text=value[0]
    return 2, text

def normalHunting(sio, data,btn_name, character_name):
  coord=data
  flag=data[4]
  name=character_name

  if flag==1:
    keyboard('7')
    result_1=client_utils.searchImg('eventObj.png',beforeDelay=2, afterDelay=10, _region=(333,245,230,300)) 
    #여기에 클릭 후 확인이라던지 있는지 없는지 확인 하고 더 만들어줘야함함

  keyboard('v')

  result_1=client_utils.searchImg('memory_place.png',beforeDelay=0, afterDelay=0, _region=(320,400,200,150)) #기억장소 메뉴 클릭
  if(result_1==0):
    return 0, "기억장소 메뉴 실패"
  client_utils.searchImg('stop_schedule.png',beforeDelay=0, afterDelay=0, chkCnt=2, _region=(1260,790,300,100))
  result_2=client_utils.searchImg('schedule_reset.png',beforeDelay=0, afterDelay=0, chkCnt=2, justChk=True,_region=(1200,790,200,200))
  if result_2!=0:
    randClick(660,345,10,10,1)  #장소 클릭
    for i in range(7):
      randClick(1540,390,0,0,0) #시간 충전
    result_3=client_utils.searchImg('clk_schedule_start.png',beforeDelay=0, afterDelay=0, _region=(1260,790,300,100))
    if result_3==1: #마을 체크
      result_village=client_utils.searchImg('portion.png',beforeDelay=4, afterDelay=0, chkCnt=11, justChk=True, _region=(340,245,200,300))
      if result_village!=0: #마을이면 5초 후 다음
        time.sleep(5)
    else:
      return 0, "스케쥴 시작 실패"
  if result_2==0:
    result_3=client_utils.searchImg('clk_schedule_start.png',beforeDelay=0, afterDelay=1, _region=(1260,790,300,100))
    if result_3==1: #마을 체크
      result_village=client_utils.searchImg('portion.png',beforeDelay=4, afterDelay=0, chkCnt=11,justChk=True, _region=(340,245,200,300))
      if result_village!=0: #마을이면 5초 후 다음
        time.sleep(5)
    else:
      return 0, "스케쥴 시작 실패"
    
  client_utils.caputure_image(name, 387, 258, sio) #name, x, y, sio
  
  return 1, "message:None"

def postBox(sio, data,btn_name, character_name):
  keyboard(',')
  
  result=client_utils.searchImg('allAccept.png',beforeDelay=1, afterDelay=2)
  if(result==0):  
    return 0, "우편 모두받기 실패"

  client_utils.searchImg('confirm.png',beforeDelay=1, afterDelay=1, accuracy=0.9, _region=(920,580,300,200))

  escKey()  #우편 나가기
  
  return 1, "message:None"

#---------던전---------#
def dungeon(sio, data, btn_name, character_name):
  coord=data
  charging=data[4]
  name=character_name
  
  if btn_name=="격전의섬":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    keyboard("`") #던전
    # result=utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    result=client_utils.searchImg('dungeonG.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "격전의 섬 클릭 실패"

    result=client_utils.searchImg('dungeon_enter.png', beforeDelay=0, afterDelay=0, _region=(1200, 750, 400, 150))  #입장하기 
    if(result==0):
      return 0, "격섬 입장 클릭 실패"
    randClick(coord[0],coord[1],coord[2],coord[3],1)  #층 클릭

  elif btn_name=="파괴된성채":
    for i in range(charging):
      keyboard("1")
      time.sleep(2)

    keyboard("`") #던전
    result=client_utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    result=client_utils.searchImg('dungeonD.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "파괴된성채 클릭 실패"

    result=client_utils.searchImg('dungeon_enter.png', beforeDelay=0, afterDelay=0, _region=(1200, 750, 400, 150))  #입장하기 
    if(result==0):
      return 0, "파괴성 입장 클릭 실패"
    randClick(coord[0],coord[1],coord[2],coord[3],1)  #층 클릭

  elif btn_name=="크루마탑":
    # for i in range(charging):
    #   keyboard("1")
    #   time.sleep(2)
    keyboard("`") #던전
    result=client_utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    result=client_utils.searchImg('cruma.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "크루마탑 클릭 실패"

    result=client_utils.searchImg('dungeon_enter.png', beforeDelay=0, afterDelay=0, _region=(1200, 750, 400, 150))  #입장하기
    if(result==0):
      return 0, "크루마 입장 클릭 실패"
    randClick(coord[0],coord[1],coord[2],coord[3],1)  #층 클릭 

  elif btn_name=="안타라스":
    print(f"{btn_name} 실행") #임시
    return 1, "message:None"
  
    # for i in range(charging):
    #     keyboard("1")
    #     time.sleep(2)

    # keyboard("`") #던전
    # result=utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    # result=utils.searchImg('antaras.png',beforeDelay=1, afterDelay=1)
    # if(result==0):
    #   return 0, "안타라스 클릭 실패"

    # result=utils.searchImg('dungeon_enter.png', beforeDelay=0, afterDelay=0, _region=(1200, 750, 400, 150))  #입장하기
    # if(result==0):
    #   return 0, "안타 입장 클릭 실패"
    # # randClick(coord[0],coord[1],coord[2],coord[3],1)  #층 클릭 (설정 해줘야함 json에서)

  elif btn_name=="상아탑":
    print(f"{btn_name} 실행") #임시
    return 1, "message:None"

    # keyboard("`") #던전
    # result=utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    # result=utils.searchImg('sanga.png',beforeDelay=1, afterDelay=1)
    # if(result==0):
    #   return 0, "상아탑 클릭 실패"

    # result=utils.searchImg('dungeon_enter.png', beforeDelay=0, afterDelay=0, _region=(1200, 750, 400, 150))  #입장하기
    # if(result==0):
    #   return 0, "상아탑 입장 클릭 실패"
    # randClick(coord[0],coord[1],coord[2],coord[3],1)  #층 클릭 (설정 해줘야함 json에서)
  elif btn_name=="이벤트던전":
    print(f"{btn_name} 실행") #임시
    return 1, "message:None"

    # keyboard("`") #던전
    # # result=utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    # result=utils.searchImg('eventDun.png',beforeDelay=1, afterDelay=1)
    # if(result==0):
    #   return 0, "이벤트던전 클릭 실패"

    # result=utils.searchImg('dungeon_enter.png', beforeDelay=0, afterDelay=0, _region=(1200, 750, 400, 150))  #입장하기
    # if(result==0):
    #   return 0, "이벤트 입장 클릭 실패"
    # # randClick(coord[0],coord[1],coord[2],coord[3],1)  #층 클릭 (설정 해줘야함 json에서)
  
  #이동 완료 체크
  result=client_utils.searchImg('chk.png', beforeDelay=1, afterDelay=1, justChk=True, chkCnt=10,_region=(910,180,230,70))
  if(result==0):
    return 0, f"{btn_name} 이동 실패"

  client_utils.caputure_image(name, 387, 258, sio) #name, x, y, sio
  keyboard('6') #순간이동

  return 1, "message:None"

#---------아이템 변경---------#
def switch_get_item(sio, data, btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("x") #환경설정
  result=client_utils.searchImg('setting_get_btn.png', beforeDelay=1, afterDelay=1, _region=(355,370,200,200))
  if(result==0):
    return 0, "세팅 획득 버튼클릭 실패"
  
  if btn_name=="모두":
    result=client_utils.searchImg('allItem.png', beforeDelay=1, afterDelay=1, _region=(1210,360,200,150))
    if(result==0):
      return 0, "모두 클릭 실패"
    
    client_utils.caputure_image(name, 1295, 400, sio) #name, x, y, sio

  elif btn_name=="고급":
    result=client_utils.searchImg('greenItem.png', beforeDelay=1, afterDelay=1, _region=(1015,400,200,150))
    if(result==0):
      return 0, "고급 클릭 실패"
    
    client_utils.caputure_image(name, 1120, 450, sio) #name, x, y, sio

  elif btn_name=="희귀":
    result=client_utils.searchImg('blueItem.png', beforeDelay=1, afterDelay=1, _region=(1190,400,200,150))
    if(result==0):
      return 0, "희귀 클릭 실패"
    
    client_utils.caputure_image(name, 1280, 450, sio) #name, x, y, sio

  escKey()  #나가기
  return 1, "message:None"

def decomposeItem(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("0") #분해
  time.sleep(1)

  randClick(1480,735,5,5,0) #분해 목록
  randClick(1395,730,10,10,0) #분해 목록 확인
  randClick(1321,735,5,5,0) #분해

  client_utils.searchImg('confirm.png', beforeDelay=1, afterDelay=1, chkCnt=2, _region=(920,580,300,200))
  
  client_utils.caputure_image(name, 1280, 340, sio) #name, x, y, sio

  return 1, "message:None"

def decomposeBook(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("9") #분해
  time.sleep(1)

  randClick(1480,735,5,5,0) #분해 목록
  randClick(1395,730,10,10,0) #분해 목록 확인
  randClick(1321,735,5,5,0) #분해

  client_utils.searchImg('confirm.png', beforeDelay=1, afterDelay=1, chkCnt=2, _region=(920,580,300,200))
  
  client_utils.caputure_image(name, 1280, 340, sio) #name, x, y, sio

  return 1, "message:None"
  
def deathChk(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name
  client_utils.searchImg('confirm.png', beforeDelay=1, afterDelay=1, chkCnt=2, _region=(920,580,300,200))

  client_utils.caputure_image(name, 1145, 195, sio) #name, x, y, sio

  return 1, "message:None"

def showDiamond(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard('x')
  # Box(left=880, top=196, width=25, height=27)
  result_1=client_utils.searchImg('diamondChk_1.png', beforeDelay=1, afterDelay=0, justChk=True, _region=(840,180,100,60), accuracy=0.7)
  result_2=client_utils.searchImg('diamondChk_2.png', beforeDelay=0, afterDelay=0, justChk=True, _region=(920,180,80,60), accuracy=0.7)
  
  if result_1!=0 and result_2!=0:
    x=result_1.left+result_1.width
    capture_width=result_2.left-x #끝나는 x좌표는 고정정
    y, height = 190, 35 
    config="--psm 7 -c tessedit_char_whitelist=0123456789,"
    binary_val=150

    text=client_utils.capture_text_from_region(x, y, capture_width, height, config,binary_val)
    if text[0]==0:  #capture_text_from_region 예외 발생
      return text[0], text[1] 
    numbers = ''.join(re.findall(r'\d+', re.sub(r"[.,]", "", text[0])))  #문자와 , . 제거 후 숫자만 남김김
    diamond=numbers
  else:
    return 0, "다이아 이미지서치 실패"
  
  escKey()  #나가기

  return 3, diamond

def useItem(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name
  
  keyboard('i') #인벤토리
  randClick(1520,735,5,5,0) 
  randClick(1450,520,10,5,0)  #일괄사용 클릭

  randClick(1305,680,5,5,0)
 
  randClick(1405,740,5,5,10) 

  return 1, "message:None"

def agasion(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("i")
  randClick(1220,460,5,5,0) #왼쪽 메뉴 클릭

  while True:
    randClick(1290,505,5,5,0) #첫 번째 카드 클릭
    randClick(1290,505,5,5,1)
    result=client_utils.searchImg('agasionFirstChk.png', beforeDelay=1, afterDelay=1, justChk=True, _region=(800,750,300,200))
    if(result==0):
      break
    for j in range(30):
      keyboard("y")
      time.sleep(1)
      keyboard("y")
      result=client_utils.searchImg('agasionExit.png', beforeDelay=1, afterDelay=1, chkCnt=3,_region=(830,775,300,140))
      if(result==1):
        break

  return 1, "message:None"

def itemDelete(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name
  
  keyboard("i")
  randClick(1225,405,5,5,0)
  randClick(1365,355,5,5,0)
  randClick(1305,740,5,5,0)
  randClick(1030,705,5,5,0)
  randClick(1055,655,5,5,0)

  randClick(1295,355,5,5,0)
  randClick(1305,740,5,5,0)
  randClick(1030,705,5,5,0)
  randClick(1055,655,5,5,2)

  result=client_utils.searchImg('chk.png', beforeDelay=1, afterDelay=1, justChk=True, chkCnt=10,_region=(910,180,230,70))
  if(result==0):
    return 0, "아이템 삭제 실패"
  
  return 1, "message:None"

def paper(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name
  
  keyboard("i")
  randClick(1225,405,10,10,0)
  randClick(1439,355,10,10,0)
  randClick(1373,737,5,5,0)
  result=client_utils.searchImg('paper_make.png', beforeDelay=1, afterDelay=1, _region=(1255,488,200,100))
  if(result==0):
    return 0, "신탁서 제작 클릭 실패"

  randClick(1230,475,5,5,2)

  for i in range(6):
    randClick(630,345,10,10,0)
    randClick(1050,825,5,5,0) #max클릭
    randClick(1450,825,10,10,1) #제작클릭

    result=client_utils.searchImg('createCancel.png', beforeDelay=1, afterDelay=1, justChk=True, _region=(1340,765,300,200))
    if(result==0):
      break
    time.sleep(3)
    randClick(945,820,10,10,1)
    randClick(945,820,10,10,0)

  escKey()  #나가기
  
  return 1, "message:None"

def event_store(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard('7')
  
  result=client_utils.searchImg('event_store.png', beforeDelay=1, afterDelay=3, chkCnt=10)  #이미지 파일 evetn_store로 이름 바꾸자
  if(result==0):
    return 0, "이벤트상점 클릭 실패"
    
  result=client_utils.searchImg('dailyProduct.png', beforeDelay=1, afterDelay=1, chkCnt=30)  #이미지 파일 evetn_store로 이름 바꾸자
  if(result==0):
    return 0, "일일상품담기 실패"
  
  for i in range(8):
    randClick(490,465,10,10,0)

  randClick(1475,830,5,5,0) #구매 결정
  randClick(1050,650,5,5,0) 
  escKey()

  result=normalHunting(sio, data,btn_name, character_name)
  return result

#거리 40M
def fourty(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("x") #환경설정

  result=client_utils.searchImg('fourty_meter.png', beforeDelay=1, afterDelay=1, _region=(1140,540,450,200)) 
  if(result==0):
    return 0, "40M 클릭 실패"

  client_utils.caputure_image(name, 1300, 720, sio) #name, x, y, sio

  escKey()  #나가기

  return 1, "message:None"

#거리 제한없음
def unlimit(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("x") #환경설정
  

  result=client_utils.searchImg('unlimit_meter.png', beforeDelay=1, afterDelay=1, _region=(1140,540,450,200)) 
  if(result==0):
    return 0, "제한없음 클릭 실패"

  client_utils.caputure_image(name, 1450,720, sio) #name, x, y, sio

  escKey()  #나가기

  return 1, "message:None"

#데일리 출석 루틴
def daily(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard(";") #출석

  #빨간색 점 없애는 루틴
  chk_y=320
  for i in range(6):
    randClick(1485,chk_y,10,10,0)
    chk_y+=80
  
  y = 255
  for i in range(6):
    region = (1530, y, 100, 70)
    
    result=client_utils.searchImg('dailyRedDotChk.png', beforeDelay=1, afterDelay=1, justChk=True, chkCnt=2, _region=region) 
    if result:
      randClick(result.left-100, result.top+30,10,10,0)
      result=client_utils.searchImg('accept.png', beforeDelay=1, afterDelay=1, _region=(1075,470,400,200)) 
      if(result==1):
        result=client_utils.searchImg('confirm.png', beforeDelay=1, afterDelay=0, _region=(920,580,300,200)) 
   
    y += 80 #y축 80씩 증가
 
  #데일리 나가기
  escKey()

  return

#혈맹 출석 루틴
def guild(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name
  keyboard('.')

  result=client_utils.searchImg('guildAttendance.png', beforeDelay=1, afterDelay=1, accuracy=0.9,_region=(500,610,300,150)) 
  if(result==0):
    randClick(1525, 200, 20, 20, 1) #나가기
    return 0, "혈맹 체크 실패"

  #기부
  randClick(915, 820, 20, 20, 0.5)
  #기본기부 받기
  i=0
  while(i<5):
    randClick(605, 720, 20, 20, 1)
    randClick(1045, 645, 20, 20, 0)
    i+=1
  #기부 나가기
  escKey()
  # randClick(1438, 305, 20, 20, 0.5)

  # 혈맹 나가기
  escKey()

  return

def store(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name
  #상점 클릭
  keyboard('u')
  time.sleep(3)
  
  result=client_utils.searchImg('adChk.png', beforeDelay=1, afterDelay=1, _region=(235,665,350,235))  #광고 체크 
  #광고 없으면 그냥 진행 (예외처리 필요 없음)
  
  #교환소 클릭
  result=client_utils.searchImg('exchange.png', beforeDelay=0, afterDelay=1)
  if(result==0):
    escKey()
    return 0, "교환소 클릭 실패"
  #일괄 구매
  randClick(1442, 850, 100, 10, 1)

  #품절 체크
  result=client_utils.searchImg('soldoutChk.png', beforeDelay=0, afterDelay=2, chkCnt=3)
  if(result==0):
    #취소 클릭
    randClick(837, 777, 100, 10, 1) 
    #상점 나가기
    randClick(1533, 200, 20, 20, 1.5)
    return

  #---레아의 성소 클릭릭
  result=client_utils.searchImg('leah_castle.png', beforeDelay=1, afterDelay=1, accuracy=0.9, _region=(1360,370,200,100)) 
  #일괄 구매
  randClick(1442, 850, 100, 10, 0.5)
  #구매
  randClick(1039, 771, 100, 10, 2.5)

  # #---사제의 의뢰 시작
  # randClick(1405, 544, 100, 10, 0.5)
  # #일괄 구매
  # randClick(1442, 850, 100, 10, 1)
  # #구매
  # randClick(1039, 771, 100, 10, 2.5)

  #상점 나가기
  escKey()

  return

#------------모닝 루틴------------#
def morning(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  # 데일리 
  daily(sio, data,btn_name, character_name)
  # #혈맹 
  guild(sio, data,btn_name, character_name)
  #상점
  store(sio, data,btn_name, character_name)

  client_utils.caputure_image(name, 387,258, sio) #name, x, y, sio

  return 1, "message:None"

def seasonpass(sio, data,btn_name, character_name):
  coord=data
  cnt=data[4]
  name=character_name

  keyboard("z") #시즌패스
  time.sleep(2)

  x_coord=700
  for i in range(cnt):
    while(True):
      result=client_utils.searchImg('getSeason.png', beforeDelay=0, afterDelay=1,_region=(1110,330,350,150))
      if(result==0):
        randClick(1325,825,10,10,0)
        result=client_utils.searchImg('confirm.png', beforeDelay=1, afterDelay=0, _region=(920,580,300,200))
        randClick(x_coord,280,30,10,1)
        break
    x_coord=x_coord+240
    
  client_utils.caputure_image(name, 1175,365, sio) #name, x, y, sio
  
  escKey()  #나가기

  return 1, "message:None"

def gameStart(sio, data,btn_name, character_name):
  pass