#skript citajuci range suborov v priecinku a exportujuci grafy spektra, intenzity, kontur f0 a ich boxploty
import parselmouth
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({'figure.max_open_warning': 0})

sns.set()
plt.rcParams['figure.dpi'] = 100 
x = 0

for i in range (0,1):
    x=x+1
    nazov_suboru = "./rozsekane/PilottoATC/{}.wav".format(x)
    snd = parselmouth.Sound(nazov_suboru)
    plt.figure()
    plt.plot(snd.xs(), snd.values.T)
    plt.xlim([snd.xmin, snd.xmax])
    plt.xlabel("time [s]")
    plt.ylabel("amplitude")
    # plt.show()
    plt.savefig("./rozsekane/PilottoATC/grafy/fqpert{}.png".format(x))
    
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
    plt.savefig("./rozsekane/PilottoATC/grafy/int{}.png".format(x))
    plt.figure()
    fig, value = plt.subplots()
    boxplot = value.boxplot(intensity.values.T, 1)
    make_labels_int(value, boxplot)
    plt.grid(False)
    plt.ylim(30,100)
    plt.ylabel("intensity [dB]")
    # plt.show()
    plt.savefig("./rozsekane/PilottoATC/grafy/BPint{}.png".format(x))
    
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
    plt.savefig("./rozsekane/PilottoATC/grafy/fund{}.png".format(x))
    
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
    plt.savefig("./rozsekane/PilottoATC/grafy/BPfund{}.png".format(x))

