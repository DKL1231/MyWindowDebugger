from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class debugger():
    def __init__(self):
        pass
    
    def load(self, path_to_exe):
        # dwCreation 플래그를 이용해 프로세스를 어떻게 생성할 것인지 판단
        # GUI를 보고자 한다면 creation_flags를 CREATE_NEW_CONSOLE로 설정하면 됨
        creation_flags = DEBUG_PROCESS
        
        # 구조체 인스턴스화
        startupinfo         = STARTUPINFO()
        process_information = PROCESS_INFORMATION()
        
        # 다음의 두 옵션은 프로세스가 독립적인 창으로 실행되게 만듦.
        # startupinfo 구조체의 설정 내용에 따라 디버거 프로세스에 미치는 영향을 보여줌
        startupinfo.dwFlags     = 0x1
        startupinfo.wShowWindow = 0x0
        
        # cb 변수 값 초기화 (cb 변수는 startupinfo 구조체의 크기를 나타냄)
        startupinfo.cb = sizeof(startupinfo)
        
        if kernel32.CreateProcessA(path_to_exe,
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            print("[*] We have sucessfully launched the process!")
            print("[*] PID: %d" %(process_information.dwProcessId))
        else:
            print("[*] Error: 0x%08x." %(kernel32.GetLastError()))
            