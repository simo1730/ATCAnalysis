import webrtcvad
import matplotlib.pyplot as plt
import pandas as pd
import parselmouth
import seaborn as sns

plt.rcParams.update({'figure.max_open_warning': 0})

sns.set()
plt.rcParams['figure.dpi'] = 100 
x = 0

vad = webrtcvad.Vad()
vad.set_mode(2) #MOD 2!!!!!!!!!!!!!
sample_rate = 8000
frame_duration = 30#ms

frame_const = int(sample_rate * frame_duration / 1000)

two_bytes = False
byte_cache = b""

frames = 0
true_frames = 0
false_frames = 0

database = pd.DataFrame()


### 000 okno ticha napr. sek polsek. prah kolko 0 je alebo neni rec

with open("./rozsekane/PilottoATC/1.wav", "rb") as f:
    while (byte := f.read(1)):
        byte_cache += byte
        
        if two_bytes:
            # print(str(byte_cache))
            frame = byte_cache * frame_const
            speech_present = vad.is_speech(frame, sample_rate)
            frames += 0.000125
            if speech_present:
                true_frames += 1
            else:
                false_frames += 1
            # print(f"Contains speech: { speech_present } ")
            byte_cache = b""
            dct = {
                "Frame": frames,
                "Voice Detected": speech_present}
            database = database.append(dct, ignore_index=True)

        two_bytes = not two_bytes

print(f"True: {true_frames}")
print(f"False: {false_frames}")
print(frames)
print(database)

nazov_suboru = "./rozsekane/PilottoATC/1.wav"
snd = parselmouth.Sound(nazov_suboru)
plt.figure()
plt.plot(snd.xs(), snd.values.T)
plt.xlim([snd.xmin, snd.xmax])
plt.xlabel("time [s]")
plt.ylabel("amplitude")


ax = plt.gca()
ax.grid(False)
database.plot(kind='line',x='Frame',y='Voice Detected',ax=ax, linewidth=1, color='r')
plt.show()


# plt.plot([0, frames], 1, 'ro')
# # plt.axis([0, 6, 0, 20])
# plt.ylabel('some numbers')
# plt.show()