# # Python program to translate
# # speech to text and text to speech


# import speech_recognition as sr
# import pyttsx3

# # Initialize the recognizer
# r = sr.Recognizer()

# # Function to convert text to
# # speech
# def SpeakText(command):
 
#  # Initialize the engine
#  engine = pyttsx3.init()
#  engine.say(command)
#  engine.runAndWait()
 
 
# # Loop infinitely for user to
# # speak




# while 1:
#  print("*"*15,"Menu","*"*15)
#  print("1. Speech to text")
#  print("2. Exit")
#  ch = int(input("Enter YOur choice:"))
#  if ch == 1:
#   try:
#     with sr.Microphone() as source:
#     # read the audio data from the default microphone
#         audio_data = r.record(source, duration=5)
#         print("Recognizing...")
#         # convert speech to text
#         # text = r.recognize_google(audio_data)
#         text = r.recognize_google(audio_data, language="es-ES")
#         print(text)
#     #   # use the microphone as source for input.
#     #   with sr.Microphone() as source2:
#     #       # wait for a second to let the recognizer
#     #       # adjust the energy threshold based on
#     #       # the surrounding noise level
#     #       r.adjust_for_ambient_noise(source2, duration=0.2)

#     #       #listens for the user's input
#     #       audio2 = r.listen(source2)

#     #       # Using google to recognize audio
#     #       MyText = r.recognize_google(audio2)
#     #       MyText = MyText.lower()

#     #       print("Did you say "+MyText)
#     #       SpeakText(MyText)

#   except sr.RequestError as e:
#       print("Could not request results; {0}".format(e))

#   except sr.UnknownValueError:
#       print("unknown error occured")

#  elif ch == 2:
#   print("Thank You :)")
#   break

 
#  # Exception handling to handle
#  # exceptions at the runtime
 
#import library
# import torch
# import librosa
# import numpy as np
# import soundfile as sf
# from scipy.io import wavfile
# from IPython.display import Audio
# from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer


# tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
# model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# file_name = 'my-audio.wav'

# data = wavfile.read(file_name)
# framerate = data[0]
# sounddata = data[1]
# time = np.arange(0,len(sounddata))/framerate
# input_audio, _ = librosa.load(file_name, sr=16000)
# input_values = tokenizer(input_audio, return_tensors="pt").input_values
# logits = model(input_values).logits
# predicted_ids = torch.argmax(logits, dim=-1)
# transcription = tokenizer.batch_decode(predicted_ids)[0]
# print(transcription)
# import speech_recognition as sp
# recognizer = sp.Recognizer()
# recognizer.energy_threshold = 30000

# with sp.Microphone() as start:
#     print("speak up!")
#     audio = recognizer.listen(start)

# # write audio to a WAV file
# with open("microphone-results.wav", "wb") as f:
#     f.write(audio.get_wav_data())

# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch


# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# # Let's chat for 5 lines
# for step in range(5):
#     # encode the new user input, add the eos_token and return a tensor in Pytorch
#     new_user_input_ids = tokenizer.encode(input(">> User:") + tokenizer.eos_token, return_tensors='pt')

#     # append the new user input tokens to the chat history
#     bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

#     # generated a response while limiting the total chat history to 1000 tokens, 
#     chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

#     # pretty print last ouput tokens from bot
#     print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))


from transformers import DistilBertTokenizer, DistilBertModel
import torch

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertModel.from_pretrained("distilbert-base-uncased")

inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
outputs = model(**inputs)

last_hidden_states = outputs.last_hidden_state