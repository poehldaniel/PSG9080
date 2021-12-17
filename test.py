from psg9080 import PSG9080

awg = PSG9080()
awg.connect()
print(awg.isConnected())

# awg.waveform(channel=1, waveform="Pulse")
# awg.frequency(channel=1, frequency=1000, unit="Hz")
# awg.amplitude(channel=1, amplitude=5, unit="V")
# awg.offset(channel=1, offset=2.5)
# awg.duty_cycle(channel=1, duty_cycle=5)
# awg.phase(channel=1, phase=0)
# awg.on(channel=1)

awg.disconnect()
print(awg.isConnected())
