import requests

api_url = "http://localhost:8080/transcribe"

audio_file_path = 'test_audio_file.m4a'

with open(audio_file_path, 'rb') as file:
  response = requests.post(api_url, files={'audio': file})

if response.status_code == 200: 
  transcription = response.json()['text']
  print('Transcription:', transcription)
else:
  print('Error:', response.json()['error']) 

return response.status_code
