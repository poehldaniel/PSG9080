from psg9080 import PSG9080

awg = PSG9080("COM7")
awg.connect()
print(awg.is_connected())

# awg.waveform(channel=1, waveform="Pulse")
# awg.frequency(channel=1, frequency=1000, unit="Hz")
# awg.amplitude(channel=1, amplitude=3, unit="V")
# awg.offset(channel=1, offset=2.5)
# awg.duty_cycle(channel=1, duty_cycle=5.0)
# awg.phase(channel=1, phase=0.0)
# awg.off(channel=1)

awg.disconnect()
print(awg.is_connected())
