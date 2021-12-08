from pydub import AudioSegment
x=0

with open('stampsfromatted.txt') as f:
   for line in f:
       if line.startswith('PA1'):
           linez = next(f)
           x=x+1
           var1, var2 = linez.split()
           var1 = float(var1)
           var2 = float(var2)
           print(var1, var2)
           var1 = var1 * 1000 
           var2 = var2 * 1000
           newAudio = AudioSegment.from_wav("bos.wav")
           newAudio = newAudio[var1:var2]
           output = "./rozsekane/ATCtoPilot/{}.wav".format(x)
           newAudio.export(output, format="wav")

x=0        

with open('stampsfromatted.txt') as f:
   for line in f:       
       if line.startswith('AP1'):
           linez = next(f)
           x=x+1
           var1, var2 = linez.split()
           var1 = float(var1)
           var2 = float(var2)
           print(var1, var2)
           var1 = var1 * 1000 
           var2 = var2 * 1000
           newAudio = AudioSegment.from_wav("bos.wav")
           newAudio = newAudio[var1:var2]
           output = "./rozsekane/PilottoATC/{}.wav".format(x)
           newAudio.export(output, format="wav")


