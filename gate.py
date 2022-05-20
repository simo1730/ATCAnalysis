from scipy.io import wavfile
import noisereduce as nr

x=1

for i in range (0,1000):
    x=x+1
    rate, data = wavfile.read("./rozsekane/ATCtoPilot/{}.wav".format(x))
    reduced_noise = nr.reduce_noise(y=data, sr=8000)
    wavfile.write(("./rozsekane/ATCtoPilot/{}gate.wav".format(x)), rate, reduced_noise)
