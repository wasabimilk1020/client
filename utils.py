import pyautogui
import time
import pyautogui
import datetime
import base64
import shell
import win32gui

#이미지 서치
def searchImg(imgTitle, beforeDelay, afterDelay, justChk=False, coord=[], chkCnt=5, _region=(300, 125, 1370, 790), accuracy=0.85):
  chkInterval=0.5
  loopCnt = 0
  while loopCnt < chkCnt:
    loopCnt += 1
    try:
      time.sleep(beforeDelay)
      result = pyautogui.locateOnScreen("./img/" + imgTitle, region=_region, confidence=accuracy)

      # 이미지 찾기 성공
      if coord:  # 이미지가 아닌 다른 곳 클릭 시
        randClick(coord[0], coord[1], coord[2], coord[3], 0)
      elif justChk:  # 클릭 없이 이미지 체크만 할 경우
        return result
      else:  # 이미지 클릭
        randClick(result[0], result[1], result[2], result[3], 0)

      time.sleep(afterDelay)
      return 1
    except pyautogui.ImageNotFoundException:  #이미지 찾기 실패
      print(f"Image '{imgTitle}' not found on screen.")
      time.sleep(chkInterval)
      continue
    except Exception as e:
      print(f"An error occurred: {e}")
      return 0 
  return 0  

def caputure_image(name,x,y,sio):
  pyautogui.screenshot(f"image_files\capture_img\{name}.png", region=(x,y,50,30))
  with open(f"image_files\capture_img\{name}.png", "rb") as f:
    b64_string = base64.b64encode(f.read())
    captureImg=b64_string
  now = datetime.datetime.now()
  nowDatetime=now.strftime('%H:%M')
  data=[name, nowDatetime, captureImg] 
  sio.emit("captured_image",data)

def getWindow(accStatus):
  # winKey()
  startClick(0,0,0,0,0)
  time.sleep(0.1)
  shell.SendKeys('%')
  try:
    win32gui.SetForegroundWindow(accStatus)
  except Exception as e:
    print(f"Error bringing window to foreground: {e}")