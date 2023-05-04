from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan, set_seed
from datasets import load_dataset
import torch
import soundfile as sf
from datasets import load_dataset
import server
import base64
from io import BytesIO

    
def generate(prompt: str, config: server.VoiceConfig) -> str:
    set_seed(config.seed)
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

    # load xvector containing speaker's voice characteristics from a dataset
    embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
    speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
    
    inputs = processor(text=prompt, return_tensors="pt")
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
    buffered = BytesIO()
    sf.write(buffered, speech.numpy(), samplerate=config.samplerate, format="mp3")

    return base64.b64encode(buffered.getvalue()).decode("utf-8")