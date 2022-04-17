#Skript exportujuci spectrogram, centroid a slope
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import pyACA

filename = "./rozsekane/PilottoATC/1.wav"
y, sr = librosa.load(filename)


# D = librosa.stft(y)
# S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
# plt.figure()
# librosa.display.waveshow(S_db)

D = librosa.stft(y)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
fig, ax = plt.subplots()
D_highres = librosa.stft(y, hop_length=256, n_fft=4096)
S_db_hr = librosa.amplitude_to_db(np.abs(D_highres), ref=np.max)
img = librosa.display.specshow(S_db_hr, hop_length=256, x_axis='time', y_axis='log',
                               ax=ax)
ax.set(title='Spectrogram')
fig.colorbar(img, ax=ax, format="%+2.f dB")

[v, t] = pyACA.computeFeatureCl(filename, "SpectralCentroid")
plt.figure()
plt.xlabel("time [s]")
plt.ylabel("centroid [Hz]")
plt.plot(t,v)


[v, t] = pyACA.computeFeatureCl(filename, "SpectralSlope")
plt.figure()
plt.xlabel("time [s]")
plt.ylabel("slope [Hz]")
plt.plot(t,v)



