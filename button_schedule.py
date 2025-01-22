import time
ERR_MSG = 0
STATUS_MSG = 1

def postBox(sio, data, id):
  character_name=id
  print("우편함")
  print("data: ", data)
  sio.emit("logEvent",["우편실행", character_name, ERR_MSG])
  time.sleep(1)

def dungeon(sio, data):
  print("격전의 섬")