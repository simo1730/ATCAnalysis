from pydub import AudioSegment
x=0

with open('stampsfromatted.txt') as f:
   for line in f:
       x=x+1
       var1, var2 = line.split()
       var1 = float(var1)
       var2 = float(var2)
       print(var1, var2)
       var1 = var1 * 1000 
       var2 = var2 * 1000
       newAudio = AudioSegment.from_wav("bos.wav")
       newAudio = newAudio[var1:var2]
       output = "./rozsekane/{}.wav".format(x)
       newAudio.export(output, format="wav")


