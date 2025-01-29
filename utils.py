import pyautogui
import time
import pyautogui
import datetime
import base64
import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")
import win32gui
from serial_comm import *
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import ImageGrab,ImageEnhance,Image,ImageOps

#이미지 서치
def searchImg(imgTitle, beforeDelay, afterDelay, justChk=False, coord=[], chkCnt=5, _region=(300, 125, 1370, 790), accuracy=0.85):
  chkInterval=0.5
  loopCnt = 0
  while loopCnt < chkCnt:
    loopCnt += 1
    try:
      time.sleep(beforeDelay)
      result = pyautogui.locateOnScreen("./image_files/" + imgTitle, region=_region, confidence=accuracy)
      
      if result is None:  # 이미지 찾기 실패
        time.sleep(chkInterval)
        continue

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
  time.sleep(0.2)
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

def capture_text_from_region(x, y, width, height, _config):
  # 화면의 특정 영역 캡처
  bbox = (x, y, x + width, y + height)
  screenshot = ImageGrab.grab(bbox)
  screenshot.save("test1.png")
  # 전처리: 흑백 변환 및 대비 증가
  grayscale = screenshot.convert("L")  # 흑백 이미지로 변환
  grayscale.save("test2.png")
  enhanced = ImageEnhance.Contrast(grayscale).enhance(2.0)  # 대비 조정
  enhanced.save("test3.png")
  binary = enhanced.point(lambda x: 0 if x < 128 else 255, '1')  # 이진화 처리
  binary.save("test4.png")
  # 크기 키우기 (2배 확대)
  scaled = binary.resize((binary.width * 2, binary.height * 2), Image.Resampling.LANCZOS)
  scaled.save("test5.png")  # 크기 조정된 이미지 저장

  # 이미지 반전
  inverted_image = ImageOps.invert(scaled)
  inverted_image.save("test6.png")

  # OCR로 문자 추출
  text = pytesseract.image_to_string(inverted_image, lang='kor',config=_config)  

  return text

