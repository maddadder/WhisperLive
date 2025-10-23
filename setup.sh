python3 -m venv ./venv
source venv/bin/activate
pip install huggingface-hub

mkdir -p models/whisper-medium
huggingface-cli download \
  --repo-type model \
  ctranslate2-4you/distil-whisper-medium.en-ct2-float32 \
  --local-dir models/whisper-medium \
  --local-dir-use-symlinks False
#which was found here: https://huggingface.co/ctranslate2-4you/distil-whisper-medium.en-ct2-float32


#to debug, exec into server:
python
>>>
from faster_whisper import WhisperModel
# Specify the model path correctly
model = WhisperModel("/app/models/whisper-medium")
