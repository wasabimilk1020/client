import time
import win32gui
import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import ImageGrab
from serial_comm import *
from utils import *

# 현재 실행중인 윈도우 핸들 목록 가져오기
def get_lin2m_hwnd_list():
  lin2m_handle_list=[]  #린2m 핸들 리스트

  def callback(_hwnd, _result: list):
    title = win32gui.GetWindowText(_hwnd)
    if win32gui.IsWindowEnabled(_hwnd) and win32gui.IsWindowVisible(_hwnd) and title is not None and len(title) > 0:
      _result.append(_hwnd)
    return True
  hwnd_list = []  #윈도우 핸들 리스트트
  win32gui.EnumWindows(callback, hwnd_list)
  
  for hwnd in hwnd_list:
    title = win32gui.GetWindowText(hwnd)
    result = title.split(' ')[0].strip()
    if result == "리니지2M":
      lin2m_handle_list.append(hwnd)
  return lin2m_handle_list

def capture_text_from_region(x, y, width, height):
  """
  주어진 좌표 (x, y)와 크기 (width, height)의 영역에서 문자를 추출
  """
  # 화면의 특정 영역 캡처
  bbox = (x, y, x + width, y + height)
  screenshot = ImageGrab.grab(bbox)
  # screenshot.save("captured_region.png")  #잘 찍히는지 확인 용

  # OCR로 문자 추출
  text = pytesseract.image_to_string(screenshot, lang='ENG+KOR',config='--psm 4 -c preserve_interword_spaces=1')  # 언어 설정 (예: 'kor' 또는 'eng+kor')
  return text

def get_account_list(sio):
  account_dict={} #{"아이디":handle value}
  lin2m_handle_list=get_lin2m_hwnd_list()

  for lin2m_hwnd in lin2m_handle_list:
    # print("핸들 값",lin2m_hwnd)
    startClick(0,0,0,0,0)
    time.sleep(0.1)
    shell.SendKeys('%')
    try:
      win32gui.SetForegroundWindow(lin2m_hwnd)
    except Exception as e:
      print(f"Error bringing window to foreground: {e}")
       
    dragValues={'fromStartX':900, 'toStartX':1015,'fromStartY':590,'toStartY':620,'fromEndX':860, 'toEndX':1000,'fromEndY':325,'toEndY':345}
    mouseDrag(dragValues)
    time.sleep(2)   #실제로는 열렸는지 확인하는 코드 넣어야됨
    keyboard('x')
    time.sleep(1)
    result=searchImg('information.png',chkCnt=10,_region=(1330, 225, 200, 100))
    if(result==0):
      print("정보 클릭 실패패")
      return
    
    x, y, width, height = 1205, 340, 120, 30
    # 문자 추출 실행
    extracted_text = capture_text_from_region(x, y, width, height)
    name=extracted_text.split(' ')[0].strip()
    account_dict[name]=lin2m_hwnd
    print(name)    
    escKey() 
    #절전모드
    keyboard('g')
    randClick(960,535,20,20,1)
    sio.emit("logEvent",["어카운트 완료", name, 1])

  return account_dict
