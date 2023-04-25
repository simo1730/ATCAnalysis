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
vad.set_mode(0) #MOD 2!!!!!!!!!!!!!
sample_rate = 8000
frame_duration = 30#ms

frame_const = int(sample_rate * frame_duration / 1000)


database = pd.DataFrame()

longest_pauses = []
longest_speeches = []
s2prs = []

for i in range (0,1):
    ### 000 okno ticha napr. sek polsek. prah kolko 0 je alebo neni rec
    x=x+1
    two_bytes = False
    byte_cache = b""
    longest_speech = 0
    longest_pause = 0
    current_speech = 0
    current_pause = 0
    frames = 0
    true_frames = 0
    false_frames = 0
    
    
    with open(("./rozsekane/ATCtoPilot/{}gate.wav".format(x)), "rb") as f:
        while (byte := f.read(1)):
            byte_cache += byte
            
            if two_bytes:
                # print(str(byte_cache))
                frame = byte_cache * frame_const
                speech_present = vad.is_speech(frame, sample_rate)
                frames += 0.000125
                if speech_present:
                    true_frames += 1
                    
                    current_speech += 1
                    current_pause = 0
                    
                    if current_speech > longest_speech:
                        longest_speech = current_speech
                    
                else:
                    false_frames += 1
                    
                    current_pause += 1
                    current_speech = 0
                    
                    if current_pause > longest_pause:
                        longest_pause = current_pause
                    
                    
                # print(f"Contains speech: { speech_present } ")
                byte_cache = b""
                dct1 = {
                    "čas [s]": frames,
                    "detekovaná reč": speech_present}
                database = database.append(dct1, ignore_index=True)
    
            two_bytes = not two_bytes
            
    s2pr = true_frames / false_frames
    # s2prs.append(s2pr)
    # longest_speeches.append(longest_speech)
    # longest_pauses.append(longest_pause)

    print(f"True: {true_frames}")
    print(f"False: {false_frames}")
    print(frames)
    print(database)
    
    nazov_suboru = "./rozsekane/ATCtoPilot/{}.wav".format(x)
    snd = parselmouth.Sound(nazov_suboru)
    plt.figure()
    plt.plot(snd.xs(), snd.values.T)
    plt.xlim([snd.xmin, snd.xmax])
    plt.xlabel("čas [s]")
    plt.ylabel("amplitúda")
    
    ax = plt.gca()
    ax.grid(False)
    database.plot(kind='line',x='čas [s]',y='detekovaná reč',ax=ax, linewidth=1, color='r')
    plt.show()
    
    matrixdata = pd.read_csv('matrixdata.csv')
    dct = {
        "Longest Speech": longest_speech,
        "Longest Pause": longest_pause,
        "s2pr": s2pr,
        }

    print(longest_speech)
    print(longest_pause)

    print (matrixdata)

    matrixdata = matrixdata.append(dct, ignore_index=True)


    matrixdata.to_csv('matrixdata.csv')
