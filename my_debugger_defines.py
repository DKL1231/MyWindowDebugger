from ctypes import *

# ctypes 형태의 타입을 마이크로소프트의 타입으로 매핑
WORD        = c_ushort
DWORD       = c_ulong
LPBYTE      = POINTER(c_ubyte)
LPTSTR      = POINTER(c_char)
HANDLE      = c_void_p
PVOID       = c_void_p
UINT_PTR    = c_ulong

#상수
DEBUG_PROCESS           = 0x00000001
CREATE_NEW_CONSOLE      = 0x00000010
PROCESS_ALL_ACCESS      = 0x001F0FFF
INFINITE                = 0xFFFFFFFF
DBG_CONTINUE            = 0x00010002

# CreateProcessA() 함수를 위한 구조체
class STARTUPINFO(Structure):
    _fields_ = [
        ("cb",              DWORD),
        ("lpReserved",      LPTSTR),
        ("lpDesktop",       LPTSTR),
        ("lpTitle",         LPTSTR),
        ("dwX",             DWORD),
        ("dwY",             DWORD),
        ("dwXSize",         DWORD),
        ("dwYSize",         DWORD),
        ("dwXCountChars",   DWORD),
        ("dwYCountChars",   DWORD),
        ("dwFillAttribute", DWORD),
        ("dwFlags",         DWORD),
        ("wShowWindow",     WORD),
        ("cbReserved2",     WORD),
        ("lpReserved2",     LPBYTE),
        ("hStdInput",       HANDLE),
        ("hStdOutput",      HANDLE),
        ("hStdError",       HANDLE),
    ]

class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ("hProcess",        HANDLE),
        ("hThread",         HANDLE),
        ("dwProcessId",     DWORD),
        ("dwThreadId",      DWORD),
    ]

class EXCEPTION_RECORD(Structure):
    pass
    
EXCEPTION_RECORD._fields_ = [
        ("ExceptionCode",        DWORD),
        ("ExceptionFlags",       DWORD),
        ("ExceptionRecord",      POINTER(EXCEPTION_RECORD)),
        ("ExceptionAddress",     PVOID),
        ("NumberParameters",     DWORD),
        ("ExceptionInformation", UINT_PTR * 15),
    ]

class _EXCEPTION_RECORD(Structure):
    _fields_ = [
        ("ExceptionCode",        DWORD),
        ("ExceptionFlags",       DWORD),
        ("ExceptionRecord",      POINTER(EXCEPTION_RECORD)),
        ("ExceptionAddress",     PVOID),
        ("NumberParameters",     DWORD),
        ("ExceptionInformation", UINT_PTR * 15),
    ]

class EXCEPTION_DEBUG_INFO(Structure):
    _fields_ = [
        ("ExceptionRecord",    EXCEPTION_RECORD),
        ("dwFirstChance",      DWORD),
    ]

class DEBUG_EVENT_UNION(Union):
    _fields_ = [
        ("Exception",         EXCEPTION_DEBUG_INFO),
#        ("CreateThread",      CREATE_THREAD_DEBUG_INFO),
#        ("CreateProcessInfo", CREATE_PROCESS_DEBUG_INFO),
#        ("ExitThread",        EXIT_THREAD_DEBUG_INFO),
#        ("ExitProcess",       EXIT_PROCESS_DEBUG_INFO),
#        ("LoadDll",           LOAD_DLL_DEBUG_INFO),
#        ("UnloadDll",         UNLOAD_DLL_DEBUG_INFO),
#        ("DebugString",       OUTPUT_DEBUG_STRING_INFO),
#        ("RipInfo",           RIP_INFO),
    ]

class DEBUG_EVENT(Structure):
    _fields_ = [
        ("dwDebugEventCode", DWORD),
        ("dwProcessId",      DWORD),
        ("dwThreadId",       DWORD),
        ("u",                DEBUG_EVENT_UNION),
    ]