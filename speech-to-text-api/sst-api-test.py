import requests

def main():
  api_url = "https://str-api-qii5r7a7fq-uc.a.run.app/transcribe"

  audio_file_path = 'test_audio_file.m4a'

  with open(audio_file_path, 'rb') as file:
    response = requests.post(api_url, files={'audio': file})

  if response.status_code == 200: 
    transcription = response.json()['text']
    print('Transcription:', transcription)
  else:
    print('Error:', response.json()['error']) 

  return response.status_code

if __name__ == "__main__":
  main()