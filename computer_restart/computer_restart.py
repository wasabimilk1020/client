import subprocess

bat_script = r"C:\경로\run_as_admin.bat"

# 관리자 권한으로 실행
subprocess.run(["cmd.exe", "/c", "start", "run_as_admin.bat"], shell=True)

