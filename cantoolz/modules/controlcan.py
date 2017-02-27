from ctypes import *
import os


class VCI_BOARD_INFO(Structure):
	_fields_=[('hw_Version', c_ushort),  
                  ('fw_Version', c_ushort),  
                  ('dr_Version', c_ushort),  
                  ('in_Version', c_ushort),  
                  ('irq_Num', c_ushort),  
                  ('can_Num', c_ubyte),  
                  ('str_Serial_Num', c_char * 20),  
                  ('str_hw_Type', c_char * 40),  
                  ('Reserved', c_ushort * 4)] 

class VCI_CAN_OBJ(Structure):
	_fields_=[('ID', c_uint),  
                  ('TimeStamp', c_uint),  
                  ('TimeFlag', c_ubyte),  
                  ('SendType', c_ubyte),  
                  ('RemoteFlag', c_ubyte),  
                  ('ExternFlag', c_ubyte),  
                  ('DataLen', c_ubyte),  
                  ('Data', c_ubyte * 8),   # can't use c_char 
                  ('Reserved', c_ubyte * 3)] 

class VCI_INIT_CONFIG(Structure):
	_fields_=[('AccCode', c_int),  
                  ('AccMask', c_int),  
                  ('Reserved', c_int),  
                  ('Filter', c_ubyte),  
                  ('Timing0', c_ubyte),  
                  ('Timing1', c_ubyte),  
                  ('Mode', c_ubyte)] 


libControlCan = cdll.LoadLibrary(os.getcwd() + "/libcontrolcan.so")


def VCI_OpenDevice(DevType=4, DevIndex=0, Reserved=0):
	OpenDevice = libControlCan.VCI_OpenDevice
	OpenDevice.argtypes = [c_int, c_int, c_int]
	OpenDevice.restypes = c_int
	returnValue = OpenDevice(DevType, DevIndex, Reserved)
	return returnValue

def VCI_CloseDevice(DevType=4, DevIndex=0):
        CloseDevice = libControlCan.VCI_CloseDevice
        CloseDevice.argtypes = [c_int, c_int]
        CloseDevice.restypes = c_int
        returnValue = CloseDevice(DevType, DevIndex)
        return returnValue

def VCI_InitCAN(DevType=4, DevIndex=0, CANIndex=0, ref_VCI_INIT_CONFIG=byref(VCI_INIT_CONFIG())):
        """The parameter ref_VCI_INIT_CONFIG is a reference to the object 
	   of class VCI_INIT_CONFIG , If we define an object like this:
	   obj1 = VCI_INIT_CONFIG()
	   The parameter ref_VCI_INIT_CONFIG can be assigned to byref(obj1)"""
        InitCAN = libControlCan.VCI_InitCAN
        #InitCAN.argtypes = [c_int, c_int, c_int, ]
        InitCAN.restypes = c_int
        returnValue = InitCAN(DevType, DevIndex, CANIndex, ref_VCI_INIT_CONFIG)
        return returnValue

def VCI_ReadBoardInfo(DevType=4, DevIndex=0, ref_VCI_BOARD_INFO=byref(VCI_BOARD_INFO())):
        """The parameter ref_VCI_BOARD_INFO is a reference to the object 
           of class VCI_BOARD_INFO , If we define an object like this:
           obj2 = VCI_BOARD_INFO()
           The parameter ref_VCI_BOARD_INFO can be assigned to byref(obj2)"""
        ReadBoardInfo = libControlCan.VCI_ReadBoardInfo
        #ReadBoardInfo.argtypes = [c_int, c_int, ]
        ReadBoardInfo.restypes = c_int
        returnValue = ReadBoardInfo(DevType, DevIndex, ref_VCI_BOARD_INFO)
        return returnValue


def VCI_GetReceiveNum(DevType=4, DevIndex=0, CANIndex=0):
        GetReceiveNum = libControlCan.VCI_GetReceiveNum
        GetReceiveNum.argtypes = [c_int, c_int, c_int]
        GetReceiveNum.restypes = c_int
        returnValue = GetReceiveNum(DevType, DevIndex, CANIndex)
        return returnValue

def VCI_ClearBuffer(DevType=4, DevIndex=0, CANIndex=0):
        ClearBuffer = libControlCan.VCI_ClearBuffer
        ClearBuffer.argtypes = [c_int, c_int, c_int]
        ClearBuffer.restypes = c_int
        returnValue = ClearBuffer(DevType, DevIndex, CANIndex)
        return returnValue

def VCI_StartCAN(DevType=4, DevIndex=0, CANIndex=0):
        StartCAN = libControlCan.VCI_StartCAN
        StartCAN.argtypes = [c_int, c_int, c_int]
        StartCAN.restypes = c_int
        returnValue = StartCAN(DevType, DevIndex, CANIndex)
        return returnValue

def VCI_ResetCAN(DevType=4, DevIndex=0, CANIndex=0):
        ResetCAN = libControlCan.VCI_ResetCAN
        ResetCAN.argtypes = [c_int, c_int, c_int]
        ResetCAN.restypes = c_int
        returnValue = ResetCAN(DevType, DevIndex, CANIndex)
        return returnValue

def VCI_Transmit(DevType=4, DevIndex=0, CANIndex=0, ref_VCI_CAN_OBJ=byref(VCI_CAN_OBJ()), Length=48):
        """The parameter ref_VCI_CAN_OBJ is a reference to the object 
           of class VCI_CAN_OBJ , If we define an object like this:
           obj3 = VCI_CAN_OBJ()
           The parameter ref_VCI_CAN_OBJ can be assigned to byref(obj3)"""
        Transmit = libControlCan.VCI_Transmit
        #Transmit.argtypes = [c_int, c_int, , c_int]
        Transmit.restypes = c_int
        returnValue = Transmit(DevType, DevIndex, CANIndex, ref_VCI_CAN_OBJ, Length)
        return returnValue

def VCI_Receive(DevType=4, DevIndex=0, CANIndex=0, ref_VCI_CAN_OBJ=byref(VCI_CAN_OBJ()), Len=2500, WaitTime=0):
        """The parameter ref_VCI_CAN_OBJ is a reference to the object 
           of class VCI_CAN_OBJ , If we define an object like this:
           obj4 = VCI_CAN_OBJ()
           The parameter ref_VCI_CAN_OBJ can be assigned to byref(obj4)"""
        Receive = libControlCan.VCI_Receive
        #Receive.argtypes = [c_int, c_int, , c_int]
        Receive.restypes = c_int
        returnValue = Receive(DevType, DevIndex, CANIndex, ref_VCI_CAN_OBJ, Len, WaitTime)
        return returnValue



### Other functions and data structure ###
# right ???
class MY_ARRAY(Structure):
	_fields_=[('str_Four_Char', c_char * 4)] 
			  
class VCI_BOARD_INFO1(Structure):
	_fields_=[('hw_Version', c_ushort),  
                  ('fw_Version', c_ushort),  
                  ('dr_Version', c_ushort),  
                  ('in_Version', c_ushort),  
                  ('irq_Num', c_ushort),  
                  ('can_Num', c_ubyte),  
                  ('Reserved', c_ubyte),  
                  ('str_Serial_Num', c_char * 8),  
                  ('str_hw_Type', c_char * 16),  
                  ('str_Usb_Serial', MY_ARRAY * 4)] 

def VCI_ConnectDevice(DevType=4, DevIndex=0):
        ConnectDevice = libControlCan.VCI_ConnectDevice
        ConnectDevice.argtypes = [c_int, c_int]
        ConnectDevice.restypes = c_int
        returnValue = ConnectDevice(DevType, DevIndex)
        return returnValue

def VCI_UsbDeviceReset(DevType=4, DevIndex=0, Reserved=0):
        UsbDeviceReset = libControlCan.VCI_UsbDeviceReset
        UsbDeviceReset.argtypes = [c_int, c_int, c_int]
        UsbDeviceReset.restypes = c_int
        returnValue = UsbDeviceReset(DevType, DevIndex, Reserved)
        return returnValue

def VCI_FindUsbDevice(ref_VCI_BOARD_INFO1):
        """The parameter ref_VCI_BOARD_INFO1 is a reference to the object 
           of class VCI_BOARD_INFO1 , If we define an object like this:
           obj5 = VCI_BOARD_INFO1()
           The parameter ref_VCI_BOARD_INFO1 can be assigned to byref(obj5)"""
        FindUsbDevice = libControlCan.VCI_FindUsbDevice
        #FindUsbDevice.argtypes = [ ]
        FindUsbDevice.restypes = c_int
        returnValue = FindUsbDevice(ref_VCI_BOARD_INFO1)
        return returnValue



if "__main__" == __name__ :
	pass #receiveTest()
else:
	pass




