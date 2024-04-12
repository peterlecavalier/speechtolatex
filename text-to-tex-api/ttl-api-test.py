import requests

def main():
    api_url = 'https://ttl-api-qii5r7a7fq-uc.a.run.app/translate'

    text = 'x squared plus y squared equals z squared'

    response = requests.post(api_url, json={'text': text})

    if response.status_code == 200: 
        print(response)
        transcription = response.json()['latex']
        print('Transcription:', transcription)
    else:
        print('Error:', response.json()['error']) 

    return response.status_code

if __name__ == "__main__":
    print(main())