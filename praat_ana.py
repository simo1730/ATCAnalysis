#skript citajuci range suborov v priecinku a exportujuci grafy spektra, intenzity, kontur f0 a ich boxploty
import parselmouth
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import librosa
import librosa.display
import pyACA
import pandas as pd

plt.rcParams.update({'figure.max_open_warning': 0})

values = pd.DataFrame()
sns.set()
plt.rcParams['figure.dpi'] = 100 
x = 0
y = 0
f = open("tempoformatted.txt","r") 


tempos = []

for line in f:
    if line.startswith('AP1'):
        tempoline = next(f)
        tempo = float(tempoline)
        tempos.append(tempo)  

for i in range (0,500):
    x=x+1
    nazov_suboru = "./rozsekane/ATCtoPilot/{}.wav".format(x)
    snd = parselmouth.Sound(nazov_suboru)
    plt.figure()
    plt.plot(snd.xs(), snd.values.T)
    plt.xlim([snd.xmin, snd.xmax])
    plt.xlabel("time [s]")
    plt.ylabel("amplitude")
    # plt.show()
    plt.savefig("./rozsekane/ATCtoPilot/grafy/fqpert{}.png".format(x))
    
    def make_labels_f0(value, boxplot):
        boxes = boxplot['boxes'][0]
        caps = boxplot['caps']
        med = boxplot['medians'][0]

        median = med.get_ydata()[1]

        pc25 = boxes.get_ydata().min()
        pc75 = boxes.get_ydata().max()

        capbottom = caps[0].get_ydata()[0]
        captop = caps[1].get_ydata()[0]

        value.text(1.1, 80,
                'Median = {:6.3g}'.format(median), va='center')
        value.text(1.1, 60,
                'Spodný percentil = {:6.3g}'.format(pc25), va='center')
        value.text(1.1, 100,
                'Vrchný percentil = {:6.3g}'.format(pc75), va='center')
        value.text(1.1, 40,
                'Spodná hodnota = {:6.3g}'.format(capbottom), va='center')
        value.text(1.1, 120,
                'Vrchná hodnota = {:6.3g}'.format(captop), va='center')
        
    def make_labels_int(value, boxplot):
        boxes = boxplot['boxes'][0]
        caps = boxplot['caps']
        med = boxplot['medians'][0]

        median = med.get_ydata()[1]

        pc25 = boxes.get_ydata().min()
        pc75 = boxes.get_ydata().max()

        capbottom = caps[0].get_ydata()[0]
        captop = caps[1].get_ydata()[0]

        value.text(1.1, 60,
                'Median = {:6.3g}'.format(median), va='center')
        value.text(1.1, 50,
                'Spodný percentil = {:6.3g}'.format(pc25), va='center')
        value.text(1.1, 70,
                'Vrchný percentil = {:6.3g}'.format(pc75), va='center')
        value.text(1.1, 40,
                'Spodná hodnota = {:6.3g}'.format(capbottom), va='center')
        value.text(1.1, 80,
                'Vrchná hodnota = {:6.3g}'.format(captop), va='center')

    
    def draw_spectrogram(spectrogram, dynamic_range=70):
        X, Y = spectrogram.x_grid(), spectrogram.y_grid()
        sg_db = 10 * np.log10(spectrogram.values)
        plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='afmhot')
        plt.ylim([spectrogram.ymin, spectrogram.ymax])
        plt.xlabel("time [s]")
        plt.ylabel("frequency [Hz]")
    
    def draw_intensity(intensity):
        plt.plot(intensity.xs(), intensity.values.T, linewidth=3, color='w')
        plt.plot(intensity.xs(), intensity.values.T, linewidth=1)
        plt.grid(False)
        plt.ylim(0)
        plt.ylabel("intensity [dB]")
    
    intensity = snd.to_intensity()
    spectrogram = snd.to_spectrogram()
    plt.figure()
    draw_spectrogram(spectrogram)
    plt.twinx()
    draw_intensity(intensity)
    plt.xlim([snd.xmin, snd.xmax])
    #plt.show()
    plt.savefig("./rozsekane/ATCtoPilot/grafy/int{}.png".format(x))
    plt.figure()
    fig, value = plt.subplots()
    boxplot = value.boxplot(intensity.values.T, 1)
    make_labels_int(value, boxplot)
    plt.grid(False)
    plt.ylim(30,100)
    plt.ylabel("intensity [dB]")
    # plt.show()
    plt.savefig("./rozsekane/ATCtoPilot/grafy/BPint{}.png".format(x))
    
    def draw_pitch(pitch):
        pitch_values = pitch.selected_array['frequency']
        pitch_values[pitch_values==0] = np.nan
        plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
        plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
        plt.grid(False)
        plt.ylim(0, 230)
        plt.ylabel("fundamental frequency [Hz]")
    
    pitch = snd.to_pitch()
    
    pre_emphasized_snd = snd.copy()
    pre_emphasized_snd.pre_emphasize()
    spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=10000)
    
    plt.figure()
    draw_spectrogram(spectrogram)
    plt.twinx()
    draw_pitch(pitch)
    plt.xlim([snd.xmin, snd.xmax])
    #plt.show()
    plt.savefig("./rozsekane/ATCtoPilot/grafy/fund{}.png".format(x))
    
    pitch_values = pitch.selected_array['frequency']
    pitch_values = pitch_values[pitch_values != 0]
    plt.figure()
    fig, value = plt.subplots()
    boxplot = value.boxplot([x for x in pitch_values.T if x <= 230])
    make_labels_f0(value, boxplot)
    plt.grid(False)
    plt.ylim(0, 230)
    plt.ylabel("fundamental frequency [Hz]")
    # plt.show()
    plt.savefig("./rozsekane/ATCtoPilot/grafy/BPfund{}.png".format(x))
    
    y, sr = librosa.load(nazov_suboru)
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    fig, ax = plt.subplots()
    D_highres = librosa.stft(y, hop_length=256, n_fft=4096)
    S_db_hr = librosa.amplitude_to_db(np.abs(D_highres), ref=np.max)
    img = librosa.display.specshow(S_db_hr, hop_length=256, x_axis='time', y_axis='log',
                                   ax=ax)
    ax.set(title='Spectrogram')
    fig.colorbar(img, ax=ax, format="%+2.f dB")
    plt.savefig("./rozsekane/ATCtoPilot/grafy/Spect{}.png".format(x))

    [v, t] = pyACA.computeFeatureCl(nazov_suboru, "SpectralCentroid")
    plt.figure()
    plt.xlabel("time [s]")
    plt.ylabel("centroid [Hz]")
    plt.plot(t,v)
    plt.savefig("./rozsekane/ATCtoPilot/grafy/Centroid{}.png".format(x))


    [v, t] = pyACA.computeFeatureCl(nazov_suboru, "SpectralSlope")
    plt.figure()
    plt.xlabel("time [s]")
    plt.ylabel("slope [Hz]")
    plt.plot(t,v)
    plt.savefig("./rozsekane/ATCtoPilot/grafy/Slope{}.png".format(x))
    
        
    
    intMax = np.amax(intensity.values.T)
    intMin = np.amin(intensity.values.T)
    f0Max = np.amax(pitch_values)
    f0Min = np.amin(pitch_values)
    intMean = np.mean(intensity.values.T)
    f0Mean = np.mean(pitch_values)
    intStd = np.std(intensity.values.T)
    f0Std = np.std(pitch_values)
    spectMean = np.mean(S_db)
    spectMax = np.amax(S_db)
    spectMin = np.amin(S_db)
    spectStd = np.std(S_db)
    slope = np.mean(v)
    centroid = np.mean(t)
    tempo = tempos[i]
    dct = {
        "Intensidy Mean": intMean,
        "Intensidy Max": intMax,
        "Intensidy Min": intMin,
        "Intensity STD": intStd,
        "F0 Mean": f0Mean,
        "F0 Max": f0Max,
        "F0 Min": f0Min,
        "F0 STD": f0Std,
        "Spect Mean": spectMean,
        "Spect Max": spectMax,
        "Spect Min": spectMin,
        "Spect Std": spectStd,
        "Slope": slope,
        "Centroid": centroid,
        "Tempo": tempo
        }
    values = values.append(dct, ignore_index=True)
    print (values)
    
    
values.to_csv('matrixdata.csv')
    
