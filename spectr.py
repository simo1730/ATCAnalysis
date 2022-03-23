import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import pyACA



# 1. Get the file path to an included audio example
filename = "./rozsekane/PilottoATC/1.wav"


# 2. Load the audio as a waveform `y`
#    Store the sampling rate as `sr`
y, sr = librosa.load(filename)

# 3. Run the default beat tracker
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

# 4. Convert the frame indices of beat events into timestamps
beat_times = librosa.frames_to_time(beat_frames, sr=sr)


D = librosa.stft(y)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
plt.figure()
librosa.display.waveshow(S_db)

D = librosa.stft(y)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
plt.figure()
librosa.display.specshow(S_db)
plt.colorbar()
        

# extract feature
[v, t] = pyACA.computeFeatureCl(filename, "SpectralCentroid")

# plot feature output
plt.figure()
plt.plot(t,v)


[v, t] = pyACA.computeFeatureCl(filename, "SpectralSlope")

# plot feature output
plt.figure()
plt.plot(t,v)

sound = Waveform(path="./rozsekane/PilottoATC/1.wav", sample_rate=44100)
f0_contour = sound.f0_contour()
plt.plot(f0_contour[0])

