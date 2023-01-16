from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class debugger():
    def __init__(self):
        self.h_process          = None
        self.pid                = None
        self.debugger_active    = False
    
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
            
            # 새로 생성한 프로세스의 핸들을 구한 후 나중에 접근하기 위해 저장.
            self.h_process = self.open_process(process_information.dwProcessId)
        else:
            print("[*] Error: 0x%08x." %(kernel32.GetLastError()))
    
    def open_process(self, pid):
        # PROCESS_ALL_ACCESS = 0x001F0FFF
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return h_process
    
    def attach(self, pid):
        self.h_process = self.open_process(pid)
        
        # 프로세스에 대한 attach 시도. 실패시 호출 종료
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active    = True
            self.pid                = int(pid)
        else:
            print("[*] Unable to attach to the process.")
    
    def run(self):
        # 디버거에 대한 디버그 이벤트 처리
        while self.debugger_active == True:
            self.get_debug_event()
    
    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE
        
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            # 아직 디버그 이벤트를 처리할 핸들러 작성하지 않음. 단순히 프로세스가 실행을 계속하게 만듦.
            # input("Press a key to continue...")
            # self.debugger_active = False
            kernel32.ContinueDebugEvent( \
                debug_event.dwProcessId, \
                debug_event.dwThreadId, \
                continue_status)
    
    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print("[*] Finished debugging. Exiting...")
            return True
        else:
            print("There was an error")
            return False