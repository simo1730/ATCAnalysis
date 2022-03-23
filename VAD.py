# import collections
# import contextlib
# import sys
# import wave
# import webrtcvad
# vad = webrtcvad.Vad()
# vad.set_mode(1)

# sample_rate = 16000
# frame_duration = 10  # ms
# frame = ./rozsekane/PilottoATC/1.wav * int(sample_rate * frame_duration / 1000)
# print ('Contains speech: %s' % (vad.is_speech(frame, sample_rate)))

import webrtcvad
vad = webrtcvad.Vad()
vad.set_mode(3)

# Run the VAD on 10 ms of silence. The result should be False.
sample_rate = 8000
frame_duration = 10  # ms

# frame = ./rozsekane/PilottoATC/1.wav * int(sample_rate * frame_duration / 1000)

frame_const = int(sample_rate * frame_duration / 1000)

two_bytes = False
byte_cache = b""

true_frames = 0
false_frames = 0

with open("./rozsekane/PilottoATC/1.wav", "rb") as f:
    while (byte := f.read(1)):
        byte_cache += byte
        
        if two_bytes:
            # print(str(byte_cache))
            frame = byte_cache * frame_const
            speech_present = vad.is_speech(frame, sample_rate)
            if speech_present:
                true_frames += 1
            else:
                false_frames += 1
            # print(f"Contains speech: { speech_present } ")
            byte_cache = b""

        two_bytes = not two_bytes

print(f"True: {true_frames}")
print(f"False: {false_frames}")





# frame = b'\x00\x00' * int(sample_rate * frame_duration / 1000)
# print(f"Contains speech: { vad.is_speech(frame, sample_rate) } ")
# # print ('Contains speech: %s' % (vad.is_speech(frame, sample_rate))