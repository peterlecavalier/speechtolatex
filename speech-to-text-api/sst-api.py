import os
from flask import Flask, request, jsonify
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
from pydub import AudioSegment 

## Todo/Note:
##  - currently, only handles 1 request at a time. If we want multiple 
##    we would need to run using gunicorn or something similar for threading,
##    or we would need to batch transcription requests from multiple users
##    and return the correct transcription to the correct user

app = Flask(__name__)
processor = WhisperProcessor.from_pretrained('openai/whisper-tiny.en')
model = WhisperForConditionalGeneration.from_pretrained('openai/whisper-tiny.en')

@app.route('/transcribe', methods=['POST'])
def transcribe():
  if 'audio' not in request.files:
    return jsonify({'error': 'No audio file provided'}), 400

  audio_file = request.files['audio']
  audio_path = audio_file.filename
  audio_format = audio_path.split('.')[-1]
  audio_file.save(audio_path)
  
  # Convert to wav if not already
  if audio_format != 'wav':
    audio = AudioSegment.from_file(audio_path, format=audio_format)
    wav_path = 'temp_audio.wav'
    audio.export(wav_path, format='wav')
  else: 
    wav_path = audio_path

  # separate audio data and sampling rate
  array, sampling_rate = librosa.load(wav_path, sr=None)

  # convert to correct sampling rate if necessary
  if sampling_rate != 16000:
    array = librosa.resample(array, orig_sr = sampling_rate, target_sr = 16000)

  # process data into features and infer on model
  input_features = processor(array, sampling_rate=16000, return_tensors='pt').input_features
  pred_ids = model.generate(input_features)

  #decode prediction
  transcription = processor.batch_decode(pred_ids, skip_special_tokens=True)[0]

  return jsonify({'text': transcription}), 200

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 8080))
  app.run(debug=True, host='0.0.0.0', port = port)
  
  
