import pyaudio
import wave
import requests
import datetime
import os

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 5 # seconds to record
dev_index = 1 # device index found by p.get_device_info_by_index(ii)

ctime=datetime.datetime.now()
time=ctime.strftime('%d-%m-%Y-%H.%M.%S')
time=str(time)


wav_output_filename = 'voices/voice_'+time +'.wav'# name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
os.system('clear')
print("Rozpoczecie nagrywania...")
frames = []

# loop through stream and append audio chunks to frame array
for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk)
    frames.append(data)

print("Zakonczono nagrywanie")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()

BASE = "http://192.168.0.122:5000/sendvoice"

with open(wav_output_filename, 'rb') as file:
	print('Rozpoczecie przesylania')
	dict = {'file': file}
	r = requests.post(BASE, files=dict)
	print("Wyslano dzwiek")
	exit()
