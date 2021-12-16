import serial
import codecs


class PSG9080:

    waveforms = [
        "Sine",
        "Square",
        "Pulse",
        "Triangle",
        "Ramp",
        "CMOS",
        "DC",
        "Dev-Sine",
        "Half-Wave",
        "Full-Wave",
        "Pos-Ladder",
        "Neg-Ladder",
        "Pos-Trap",
        "Neg-Trap",
        "Noise",
        "Exp-Rise",
        "Exp-Fall",
        "Log-Rise",
        "Log-Fall",
        "Sinc",
        "Multi tone",
        "Lorenz",
    ]

    # __start_bit = ":"
    # __operator = ["w", "r"]
    # __eol = "\n"
    # function_code 0-99

    def __init__(self, port="COM7"):
        self.port = port
        self.device = None
        self.channel_state = (0, 0)

    def connect(self):
        try:
            self.device = serial.Serial(self.port, 115200, timeout=1)
            print(f"Connected to {self.port}")
        except:
            print(f"Connection failed! ({self.port})")

    def isConnected(self):
        try:
            return self.device.isOpen()
        except:
            return False

    def disconnect(self):
        try:
            return self.device.close()
        except:
            return False

    def __send(self, command):
        try:
            self.device.write(codecs.encode(command))
            response = self.device.readline()
            if "ok" in response.decode("utf-8"):
                return True
            else:
                return False
        except:
            return False

    def __receive(self):
        pass

    def on(self, channel=1):
        if channel == 1:
            self.channel_state = (1, self.channel_state[1])
        elif channel == 2:
            self.channel_state = (self.channel_state[0], 1)
        else:
            return False
        command = f":w10={self.channel_state[0]},{self.channel_state[1]}.\n"
        self.__send(command)
        return True

    def on_all(self):
        self.channel_state = (1, 1)
        command = f":w10=1,1.\n"
        self.__send(command)
        return True

    def off(self, channel=1):
        if channel == 1:
            self.channel_state = (0, self.channel_state[1])
        elif channel == 2:
            self.channel_state = (self.channel_state[0], 0)
        else:
            return False
        command = f":w10={self.channel_state[0]},{self.channel_state[1]}.\n"
        self.__send(command)
        return True

    def off_all(self):
        self.channel_state = (0, 0)
        command = f":w10=0,0.\n"
        self.__send(command)
        return True

    def waveform(self, channel=1, waveform="Sine"):
        # CH1: w11, CH2: w12
        if "Arbitrary" in waveform:
            command = f":w1{channel}={waveform[-3:]}.\n"
        else:
            command = f":w1{channel}={self.waveforms.index(waveform)}.\n"
        self.__send(command)
        return True

    def frequency(self, channel=1, frequency=1000, unit="Hz"):
        # CH1: w13, CH2: w14
        if unit == "Hz":
            unit_operator = 0
            frequency = frequency * 1000
        elif unit == "kHz" or unit == "KHz":
            unit_operator = 1
            frequency = frequency * 1000000
        elif unit == "MHz":
            unit_operator = 2
            frequency = frequency * 1000000000
        elif unit == "mHz":
            unit_operator = 3
            frequency = frequency * 1000
        elif unit == "uHz":
            unit_operator = 4
            frequency = frequency * 1000
        else:
            return False
        command = f":w1{2+channel}={frequency},{unit_operator}.\n"
        self.__send(command)
        return True

    def amplitude(self, channel=1, amplitude=1, unit="V"):
        # CH1: w15, CH2: w16
        if unit == "V":
            amplitude = amplitude * 1000
        elif unit == "mV":
            pass
        else:
            return False
        command = f":w1{4+channel}={amplitude}.\n"
        self.__send(command)
        return True

    def offset(self, channel=1, offset=1):
        # offset range: -9.99V (offset_value = 1) to +15V (offset_value = 2500)
        # CH1: w17, CH2: w18
        offset_value = 100 * offset + 1000
        command = f":w1{6+channel}={offset_value}.\n"
        self.__send(command)
        return True

    def duty_cycle(self, channel=1, duty_cycle=50):
        # duty cycle range: 0.00 (0) to 99.99 (9999)
        # CH1: w19, CH2: w20
        if channel == 1:
            command = f":w19={duty_cycle * 100}.\n"
        elif channel == 2:
            command = f":w20={duty_cycle * 100}.\n"
        else:
            return False
        self.__send(command)
        return True

    def phase(self, channel=1, phase=0):
        # phase range: 0° (0) to 359.99° (35999)
        # CH1: w21, CH2: w22
        command = f":w2{channel}={phase * 100}.\n"
        self.__send(command)
        return True

    def default(self, channel=1):
        self.waveform(channel=channel, waveform="Sine")
        self.frequency(channel=channel, frequency=100 * (10 ** channel), unit="Hz")
        self.amplitude(channel=channel, amplitude=5, unit="V")
        self.offset(channel=channel, offset=0)
        self.duty_cycle(channel=channel, duty_cycle=50)
        self.phase(channel=channel, phase=0)
        self.off_all()
        return True

    def default_all(self):
        self.default(channel=1)
        self.default(channel=2)
        return True