import time
import utils

def statusChk(sio, data,btn_name, character_name):
  print(f"{btn_name} 실행")
  time.sleep(1)
  return 1, "message:None"

def postBox(sio, data,btn_name, character_name):
  keyboard(',')
  
  result=utils.searchImg('allAccept.png',beforeDelay=1, afterDelay=2)
  if(result==0):  
    return 0, "우편 모두받기 실패"

  result=utils.searchImg('confirm.png',beforeDelay=1, afterDelay=0, accuracy=0.9, _region=(920,580,300,200))
  if(result==0):  
    return 0, "우편 확인 클릭 실패"

  escKey()  #우편 나가기
  
  return 1, "message:None"

#---------던전---------#
def dungeon(sio, data, btn_name, character_name):
  #data=[1142, 375, 10, 10, 0.0]=[x,y,xRange,yRange,delay]
  coord=data
  delay=data[4]
  name=character_name
  
  keyboard("`") #던전
  
  if btn_name=="격전의섬":
    # result=utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    result=utils.searchImg('dungeonG.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "격전의 섬 클릭 실패"

    result=utils.searchImg('dungeon_enter.png', beforeDelay=1, afterDelay=1, _region=(1200, 750, 400, 150))  #입장하기 
    if(result==0):
      return 0, "격섬 입장 클릭 실패"
    randClick(coord[0],coord[1],coord[2],coord[3],delay)  #층 클릭

  elif btn_name=="파괴된성채":
    result=utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    result=utils.searchImg('dungeonD.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "파괴된성채 클릭 실패"

    result=utils.searchImg('dungeon_enter.png', beforeDelay=1, afterDelay=1, _region=(1200, 750, 400, 150))  #입장하기 
    if(result==0):
      return 0, "파괴성 입장 클릭 실패"
    randClick(coord[0],coord[1],coord[2],coord[3],delay)  #층 클릭

  elif btn_name=="크루마탑":
    # result=utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    result=utils.searchImg('cruma.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "크루마탑 클릭 실패"

    result=utils.searchImg('dungeon_enter.png', beforeDelay=1, afterDelay=1, _region=(1200, 750, 400, 150))  #입장하기 
    if(result==0):
      return 0, "크루마 입장 클릭 실패"
    # randClick(coord[0],coord[1],coord[2],coord[3],delay)  #층 클릭 (설정 해줘야함 json에서)

  elif btn_name=="안타라스":
    result=utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    result=utils.searchImg('antaras.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "안타라스 클릭 실패"

    result=utils.searchImg('dungeon_enter.png', beforeDelay=1, afterDelay=1, _region=(1200, 750, 400, 150))  #입장하기 
    if(result==0):
      return 0, "안타 입장 클릭 실패"
    # randClick(coord[0],coord[1],coord[2],coord[3],delay)  #층 클릭 (설정 해줘야함 json에서)

  elif btn_name=="상아탑":
    print(f"{btn_name} 실행") #임시
    # result=utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    # result=utils.searchImg('sanga.png',beforeDelay=1, afterDelay=1)
    # if(result==0):
    #   return 0, "상아탑 클릭 실패"

    # result=utils.searchImg('dungeon_enter.png', beforeDelay=1, afterDelay=1, _region=(1200, 750, 400, 150))  #입장하기 
    # if(result==0):
    #   return 0, "상아탑 입장 클릭 실패"
    # randClick(coord[0],coord[1],coord[2],coord[3],delay)  #층 클릭 (설정 해줘야함 json에서)
  elif btn_name=="이벤트던전":
    print(f"{btn_name} 실행")
    # # result=utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    # result=utils.searchImg('eventDun.png',beforeDelay=1, afterDelay=1)
    # if(result==0):
    #   return 0, "이벤트던전 클릭 실패"

    # result=utils.searchImg('dungeon_enter.png', beforeDelay=1, afterDelay=1, _region=(1200, 750, 400, 150))  #입장하기 
    # if(result==0):
    #   return 0, "이벤트 입장 클릭 실패"
    # # randClick(coord[0],coord[1],coord[2],coord[3],delay)  #층 클릭 (설정 해줘야함 json에서)
  
  #이동 완료 체크
  result=utils.searchImg('chk.png', beforeDelay=1, afterDelay=1, justChk=True, chkCnt=10,_region=(910,180,230,70))
  if(result==0):
    return 0, f"{btn_name} 이동 실패"

  utils.caputure_image(name, 387, 258, sio) #name, x, y, sio
  keyboard('6') #순간이동

  return 1, "message:None"

#---------아이템 변경---------#
def switch_get_item(sio, data, btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("x") #환경설정
  time.sleep(1)

  if btn_name=="모두":
    result=utils.searchImg('setting_get_btn.png', beforeDelay=1, afterDelay=1, _region=(355,370,200,200))
    if(result==0):
      return 0, "세팅 획득 버튼클릭 실패"

    result=utils.searchImg('allItem.png', beforeDelay=1, afterDelay=1, _region=(1210,360,200,150))
    if(result==0):
      return 0, "모두 클릭 실패"
    
    utils.caputure_image(name, 1295, 400, sio) #name, x, y, sio
  elif btn_name=="고급":
    result=utils.searchImg('setting_get_btn.png', beforeDelay=1, afterDelay=1, _region=(355,370,200,200))
    if(result==0):
      return 0, "세팅 획득 버튼클릭 실패"

    result=utils.searchImg('greenItem.png', beforeDelay=1, afterDelay=1, _region=(1015,400,200,150))
    if(result==0):
      return 0, "고급 클릭 실패"
    
    utils.caputure_image(name, 1120, 450, sio) #name, x, y, sio

  elif btn_name=="희귀":
    result=utils.searchImg('setting_get_btn.png', beforeDelay=1, afterDelay=1, _region=(355,370,200,200))
    if(result==0):
      return 0, "세팅 획득 버튼클릭 실패"

    result=utils.searchImg('blueItem.png', beforeDelay=1, afterDelay=1, _region=(1190,400,200,150))
    if(result==0):
      return 0, "희귀 클릭 실패"
    
    utils.caputure_image(name, 1280, 450, sio) #name, x, y, sio

  escKey()  #나가기
  return 1, "message:None"

def decomposeItem(sio, data,btn_name, character_name):
  print(f"{btn_name} 실행")
  time.sleep(1)
  return 1, "message:None"
