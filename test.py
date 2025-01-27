import pyautogui
try:
  result = pyautogui.locateOnScreen("./image_files/test.png.")
  print(result)
except pyautogui.ImageNotFoundException:
  print("이미지 찾을 수 없음")