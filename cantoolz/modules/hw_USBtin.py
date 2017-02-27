from .controlcan import *   # My module
from cantoolz.can import *
from cantoolz.module import *
import time


class hw_USBtin(CANModule):
    name = "USBtin I/O"
    help = """

    This module to read/write with CANalyst-II
    Supporting for extended format!

    Init parameters example:

     'port' : 'auto',         # Serial port
     'debug': 2,              # debug level (default 0)
     'speed': 50              # bus speed (500, 1000)

    Module parameters:
      action - 'read' or 'write'. Will write/read to/from bus
      'pipe' -  integer, 1 by default - from which pipe to read or write

        Example: {'action':'read','pipe':2}

    """

    _serialPort = None
    _COMPort = None

    version = 1.0

    id = 6

    _bus = "USBTin"

    def read_all(self):
        #print "Call method read_all()"
        out = ""
        #VCI_Receive()
        #while self._serialPort.inWaiting() > 0:
        #    out += self._serialPort.read(1).decode("ISO-8859-1")
        return out

    def do_stop(self, params):  # disable reading
        self.dprint (1,"Call method do_stop()")
        if self._run:
            # self.dev_write(0, "C")   # disable reading
            self._run = False
        time.sleep(1)
        VCI_ClearBuffer(4, 0, 0)   # self.read_all()   # Clear Buffer

    def set_speed(self, def_in, speed):   # Only support 500 at now
        self.dprint (1,"Call method set_speed()")
        sjw_user = 3
        again = False
        if self._run:
            self._active = False
            self.do_stop({})
            again = True

        self._currentSpeed = float(speed)
        #sjw_user = self._sjw

        self.dprint (1,"Set Speed Here !")
        config = VCI_INIT_CONFIG()
        config.AccCode = 0
        config.AccMask = 0xffffffff
        config.Filter = 1
        config.Mode = 0
        if 500 == self._currentSpeed:
            # 125 Kbps  0x03  0x1C
            # 500 Kbps  0x00  0x1C
            config.Timing0 = 0x00
            config.Timing1 = 0x1C
        else:
            self.dprint(1,"Only support 500 Kbps at now")
            exit()

        if VCI_InitCAN(4, 0, 0, byref(config)) != 1:
            self.dprint (1,"Init CAN 0 Error")
            VCI_CloseDevice(4, 0)
            exit()

        if again:
            # self._run = True
            self.do_start({})
            self._active = True

        return "Speed: " + str(self._currentSpeed)

    def do_start(self, params):  # enable reading
        self.dprint (1,"Call method do_start()")

        if not self._run:
            VCI_StartCAN(4, 0, 0)
            self._run = True
            self.wait_for = False
            self.last = time.clock()
        time.sleep(1)

    def init_port(self):   # Open Device
        self.dprint (1,"Call method init_port()")
        if VCI_OpenDevice(4, 0, 0) != 1:
            self.dprint (1,'open device error')
            return 0
        else:
            self.dprint (1,'Open Device Success !')
            return 1

    def do_exit(self, params):
        VCI_CloseDevice(4, 0)

    def do_init(self, params):  # Get device and open serial port
        self.DEBUG = int(params.get('debug', 0))
        self.dprint(1,"Call method do_init()")
        self.dprint(1, "Init phase started...")
        self._bus = (params.get('bus', "USBTin"))
        self._lost_frames = 0
        if self.init_port() != 1:
            self.dprint(0, 'Can\'t init device!')
            exit()

        self._usbtin_loop = bool(params.get('usbtin_loop',False))
        self._restart = bool(params.get('auto_activate', False))
        self.act_time = float(params.get('auto_activate', 5.0))
        self.last = time.clock()
        self.wait_for = False
        self._run = True
        self.do_stop({})
        self.set_speed(0, '500')
        #self.dprint(1, "PORT: " + self._COMPort)
        self.dprint(1, "Speed: " + str(self._currentSpeed))
        self.dprint(1, "CANalyst-II device found!")

        self._cmdList['speed'] = ["Set device speed (kBaud) and SJW level(optional)", 1, " <speed>,<SJW> ", self.set_speed, True]
        self._cmdList['t'] = ["Send direct command to the device, like t001411223344", 1, " <cmd> ", self.dev_write, True]

    def dev_write(self, def_in, data):
        return ""

    def do_effect(self, can_msg, args):  # read full packet from serial port
        if args.get('action') == 'read':
            can_msg = self.do_read(can_msg)
        elif args.get('action') == 'write':
            # KOSTYL: workaround for BMW f10 bus
            #if self._restart and self._run and (time.clock() - self.last) >= self.act_time:
            #    self.dev_write(0, "O")
            #    self.last = time.clock()
            self.do_write(can_msg)
        else:
            self.dprint(1, 'Command ' + args.get('action', 'NONE') + ' not implemented 8(')
        return can_msg

    def do_read(self, can_msg):
        return can_msg

    def do_write(self, can_msg):
        return can_msg
