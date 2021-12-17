######################################################################
# Author:      DANIEL PÖHL
# Description: Framework to control the Programmable Signal Generator PSG9080
# Comments:    last changes: 2021-12-17 10:06:35
######################################################################

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
        """__init__ method

        :param port: COM port of the PSG9080, defaults to "COM7"
        :type port: str, optional
        """
        self.port = port
        self.device = None
        self.channel_state = (0, 0)

    def connect(self) -> bool:
        """connect to the selected COM port

        :return: successfully connected (True) or not (False)
        :rtype: bool
        """
        try:
            self.device = serial.Serial(self.port, 115200, timeout=1)
            print(f"Connected to {self.port}")
            return True
        except:
            print(f"Connection failed! ({self.port})")
            return False

    def disconnect(self) -> bool:
        """disconnect the PSG9080

        :return: successfully disconnected (True) or not (False)
        :rtype: bool
        """
        try:
            return self.device.close()
        except:
            return False

    def isConnected(self) -> bool:
        """check if the connection to the PSG9080 is established

        :return: connected (True) or not (False)
        :rtype: bool
        """
        try:
            return self.device.isOpen()
        except:
            return False

    def __send(self, command: str) -> bool:
        """send the desired command to the PSG9080

        :param command: desired command 
        :type command: str
        :return: sending data successfully (True) or not (False)
        :rtype: bool
        """
        assert isinstance(command, str), "command must be a string"
        try:
            self.device.write(codecs.encode(command))
            response = self.device.readline()
            if "ok" in response.decode("utf-8"):
                return True
            else:
                return False
        except:
            return False

    def __receive(self) -> bool:
        pass

    def on(self, channel=1) -> bool:
        """turn the selected channel on

        :param channel: channel to be turned on, defaults to 1
        :type channel: int, optional
        :return: turned on successfully (True) or not (False)
        :rtype: bool
        """
        assert isinstance(channel, int), "channel must be int"
        assert channel == 0 or channel == 1, "channel must be 1 or 2"
        if channel == 1:
            self.channel_state = (1, self.channel_state[1])
        elif channel == 2:
            self.channel_state = (self.channel_state[0], 1)
        else:
            return False
        command = f":w10={self.channel_state[0]},{self.channel_state[1]}.\n"
        return self.__send(command)

    def on_all(self) -> bool:
        """turning both channels on

        :return: turned on successfully (True) or not (False)
        :rtype: bool
        """
        self.channel_state = (1, 1)
        command = f":w10=1,1.\n"
        return self.__send(command)

    def off(self, channel=1) -> bool:
        """turn the selected channel off

        :param channel: channel to be turned off, defaults to 1
        :type channel: int, optional
        :return: turned off successfully (True) or not (False)
        :rtype: bool
        """
        assert isinstance(channel, int), "channel must be int"
        assert channel == 0 or channel == 1, "channel must be 1 or 2"
        if channel == 1:
            self.channel_state = (0, self.channel_state[1])
        elif channel == 2:
            self.channel_state = (self.channel_state[0], 0)
        else:
            return False
        command = f":w10={self.channel_state[0]},{self.channel_state[1]}.\n"
        return self.__send(command)

    def off_all(self) -> bool:
        """turning both channels off

        :return: turned off successfully (True) or not (False)
        :rtype: bool
        """
        self.channel_state = (0, 0)
        command = f":w10=0,0.\n"
        return self.__send(command)

    def waveform(self, channel=1, waveform="Sine") -> bool:
        """select waveform

        :param channel: desired channel, defaults to 1
        :type channel: int, optional
        :param waveform: desired waveform, defaults to "Sine"
        :type waveform: str, optional
        :return: waveform successfully selected (True) or not (False)
        :rtype: bool
        """
        assert isinstance(channel, int), "channel must be int"
        assert channel == 0 or channel == 1, "channel must be 1 or 2"
        assert isinstance(waveform, str), "waveform must be a string"
        assert waveform in self.waveforms, "waveform not known"
        # CH1: w11, CH2: w12
        if "Arbitrary" in waveform:
            command = f":w1{channel}={waveform[-3:]}.\n"
        else:
            command = f":w1{channel}={self.waveforms.index(waveform)}.\n"
        return self.__send(command)

    def frequency(self, channel=1, frequency=1000, unit="Hz") -> bool:
        """select frequency

        :param channel: desired channel, defaults to 1
        :type channel: int, optional
        :param frequency: desired frequency, defaults to 1000
        :type frequency: int, optional
        :param unit: unit of the frequency, defaults to "Hz"
        :type unit: str, optional
        :return: frequency successfully selected (True) or not (False)
        :rtype: bool
        """
        assert isinstance(channel, int), "channel must be int"
        assert channel == 0 or channel == 1, "channel must be 1 or 2"
        assert isinstance(frequency, int), "frequency must be int"
        units = ["uHz", "mHz", "Hz", "kHz", "MHz"]
        assert isinstance(unit, str), "unit must be a string"
        assert unit in units, f"unit not known, possible units: {units}"
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
        return self.__send(command)

    def amplitude(self, channel=1, amplitude=1.00, unit="V") -> bool:
        """select amplitude

        :param channel: desired channel, defaults to 1
        :type channel: int, optional
        :param amplitude: desired amplitude, defaults to 1
        :type amplitude: int, optional
        :param unit: unit of the amplitude, defaults to "V"
        :type unit: str, optional
        :return: amplitude successfully selected (True) or not (False)
        :rtype: bool
        """
        assert isinstance(channel, int), "channel must be int"
        assert channel == 0 or channel == 1, "channel must be 1 or 2"
        assert isinstance(amplitude, float), "amplitude must be int or float"
        units = ["mV", "V"]
        assert isinstance(unit, str), "unit must be a string"
        assert unit in units, f"unit not known, possible units: {units}"
        # CH1: w15, CH2: w16
        if unit == "V":
            amplitude = amplitude * 1000
        elif unit == "mV":
            pass
        else:
            return False
        command = f":w1{4+channel}={amplitude}.\n"
        return self.__send(command)

    def offset(self, channel=1, offset=1.00) -> bool:
        """select offset

        :param channel: desired channel, defaults to 1
        :type channel: int, optional
        :param offset: desired offset voltage, unit V, defaults to 1.00
        :type offset: int, optional
        :return: offset successfully selected (True) or not (False)
        :rtype: bool
        """
        assert isinstance(channel, int), "channel must be int"
        assert channel == 0 or channel == 1, "channel must be 1 or 2"
        assert isinstance(offset, float), "offset must be int or float"
        assert offset >= -9.99 and offset <= 15.00, "offset range: -9.99V to +15.00V"
        # offset range: -9.99V (offset_value = 1) to +15V (offset_value = 2500)
        # CH1: w17, CH2: w18
        offset_value = 100 * offset + 1000
        command = f":w1{6+channel}={offset_value}.\n"
        return self.__send(command)

    def duty_cycle(self, channel=1, duty_cycle=50) -> bool:
        """select duty cycle (only possible for some waveforms)

        :param channel: desired channel, defaults to 1
        :type channel: int, optional
        :param duty_cycle: desired duty cycle, defaults to 50
        :type duty_cycle: int, optional
        :return: duty cycle successfully selected (True) or not (False)
        :rtype: bool
        """
        assert isinstance(channel, int), "channel must be int"
        assert channel == 0 or channel == 1, "channel must be 1 or 2"
        assert isinstance(duty_cycle, float), "duty_cycle must be int or float"
        assert (
            duty_cycle >= 0.00 and duty_cycle <= 15.00
        ), "duty cycle range: 0.00 to 99.99"
        # duty cycle range: 0.00 (0) to 99.99 (9999)
        # CH1: w19, CH2: w20
        if channel == 1:
            command = f":w19={duty_cycle * 100}.\n"
        elif channel == 2:
            command = f":w20={duty_cycle * 100}.\n"
        else:
            return False
        return self.__send(command)

    def phase(self, channel=1, phase=0) -> bool:
        """select phase (only possible for some waveforms)

        :param channel: desired channel, defaults to 1
        :type channel: int, optional
        :param phase: desired phase shift, defaults to 0
        :type phase: int, optional
        :return: phase successfully selected (True) or not (False)
        :rtype: bool
        """
        assert isinstance(channel, int), "channel must be int"
        assert channel == 0 or channel == 1, "channel must be 1 or 2"
        assert isinstance(phase, float), "phase must be int or float"
        assert phase >= 0.00 and phase <= 359.99, "phase range: 0.00 to 359.99"
        # phase range: 0° (0) to 359.99° (35999)
        # CH1: w21, CH2: w22
        command = f":w2{channel}={phase * 100}.\n"
        return self.__send(command)

    def default(self, channel=1) -> bool:
        """reset selected channel to default values

        :param channel: desired channel, defaults to 1
        :type channel: int, optional
        :return: channel successfully set to default
        :rtype: bool
        """
        assert isinstance(channel, int), "channel must be int"
        assert channel == 0 or channel == 1, "channel must be 1 or 2"
        try:
            self.waveform(channel=channel, waveform="Sine")
            self.frequency(channel=channel, frequency=100 * (10 ** channel), unit="Hz")
            self.amplitude(channel=channel, amplitude=5, unit="V")
            self.offset(channel=channel, offset=0)
            self.duty_cycle(channel=channel, duty_cycle=50)
            self.phase(channel=channel, phase=0)
            self.off_all()
            return True
        except:
            return False

    def default_all(self) -> bool:
        """reset both channels to default values

        :return: successfully set to default
        :rtype: bool
        """
        try:
            self.default(channel=1)
            self.default(channel=2)
            return True
        except:
            return False
