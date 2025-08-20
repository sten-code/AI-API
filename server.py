from flask import Flask, request
from waitress import serve
from typing import Type
import importlib.util, tempfile, time, pathlib, os
from flask_cors import CORS

os.environ["TRANSFORMERS_CACHE"] = "./huggingface/hub"
os.environ["HF_HOME"] = "./huggingface"


debug = True
app = Flask(__name__)
CORS(app)

class Config:
    pass

class TextConfig(Config):
    max_new_tokens = 200
    do_sample = True
    temp = 1.0
    seed = 1
    numreturn = 1

class ImageConfig(Config):
    num_inference_steps = 75
    guidance_scale = 7.5
    seed = 42

class VoiceConfig(Config):
    samplerate = 16000
    seed = 42

class VideoConfig(Config):
    num_frames = 200
    seed = 42
    num_inference_steps = 25
    fps = 8


def generate_text(model: str, prompt: str, config: TextConfig) -> str:
    spec = importlib.util.spec_from_file_location("model", "models/text-generation/" + model + "/model.py")
    model = spec.loader.load_module()
    return model.generate(prompt, config)

def generate_image(model: str, prompt: str, config: ImageConfig):
    spec = importlib.util.spec_from_file_location("model", "models/image-generation/" + model + "/model.py")
    model = spec.loader.load_module()
    return model.generate(prompt, config)

def generate_voice(model: str, prompt: str, config: VoiceConfig):
    spec = importlib.util.spec_from_file_location("model", "models/voice-generation/" + model + "/model.py")
    model = spec.loader.load_module()
    return model.generate(prompt, config)

def generate_video(model: str, prompt: str, config: VideoConfig):
    spec = importlib.util.spec_from_file_location("model", "models/video-generation/" + model + "/model.py")
    model = spec.loader.load_module()
    return model.generate(prompt, config)

def get_models() -> dict[str, str]:
    output = {}
    for model_type in [f for f in pathlib.Path("./models").glob("*") if f.is_dir()]:
        output[model_type.name] = [f.name.replace("--", "/") for f in model_type.iterdir() if f.is_dir()]
    return output

@app.route("/text-generation/generate", methods=["POST"])
def text_generate():
    data = request.get_json()
    if not isinstance(data, dict):
        return {"error": "Invalid data"}

    if (prompt := data.get("prompt")) is None:
        return {"error": "Data didn't include 'prompt'."}
    if not isinstance(prompt, str):
        return {"error": "'prompt' must be a string."}

    if (model := data.get("model")) is None:
        return {"error": "Data didn't include 'model'."}
    if not isinstance(model, str):
        return {"error": "'model' must be a string."}

    models = get_models()
    if (text_models := models.get("text-generation")) is None:
        return {"error": "There are currently no models available."}
    if model not in text_models:
        return {"error": f"'{model}' isn't an available model."}
    
    cfg = parse_config(TextConfig, data)
    if isinstance(cfg, dict):
        return cfg

    model = model.replace("/", "--")
    start = time.time()
    response = generate_text(model, prompt, cfg)
    total = time.time() - start
    return {"duration": total, "response": response}

@app.route("/image-generation/generate", methods=["POST"])
def image_generate():
    data = request.get_json()
    if not isinstance(data, dict):
        return {"error": "Invalid data"}

    if (prompt := data.get("prompt")) is None:
        return {"error": "Data didn't include 'prompt'."}
    if not isinstance(prompt, str):
        return {"error": "'prompt' must be a string."}

    if (model := data.get("model")) is None:
        return {"error": "Data didn't include 'model'."}
    if not isinstance(model, str):
        return {"error": "'model' must be a string."}

    models = get_models()
    if (text_models := models.get("image-generation")) is None:
        return {"error": "There are currently no models available."}
    if model not in text_models:
        return {"error": f"'{model}' isn't an available model."}

    cfg = parse_config(ImageConfig, data)
    if isinstance(cfg, dict):
        return cfg

    model = model.replace("/", "--")
    start = time.time()
    base64 = generate_image(model, prompt, cfg)
    total = time.time() - start
    return {"duration": total, "base64": base64, "format": "data:image/jpeg;base64,"}

@app.route("/voice-generation/generate", methods=["POST"])
def voice_generate():

    data = request.get_json()
    if not isinstance(data, dict):
        return {"error": "Invalid data"}

    if (prompt := data.get("prompt")) is None:
        return {"error": "Data didn't include 'prompt'."}
    if not isinstance(prompt, str):
        return {"error": "'prompt' must be a string."}

    if (model := data.get("model")) is None:
        return {"error": "Data didn't include 'model'."}
    if not isinstance(model, str):
        return {"error": "'model' must be a string."}

    models = get_models()
    if (voice_models := models.get("voice-generation")) is None:
        return {"error": "There are currently no models available."}
    if model not in voice_models:
        return {"error": f"'{model}' isn't an available model. {models}" }

    cfg = parse_config(VoiceConfig, data)
    if isinstance(cfg, dict):
        return cfg

    model = model.replace("/", "--")
    start = time.time()
    base64 = generate_voice(model, prompt, cfg)
    total = time.time() - start
    return {"duration": total, "base64": base64, "format": "data:audio/mpeg;base64,"}

@app.route("/video-generation/generate", methods=["POST"])
def video_generate():
    data = request.get_json()
    if not isinstance(data, dict):
        return {"error": "Invalid data"}

    if (prompt := data.get("prompt")) is None:
        return {"error": "Data didn't include 'prompt'."}
    if not isinstance(prompt, str):
        return {"error": "'prompt' must be a string."}

    if (model := data.get("model")) is None:
        return {"error": "Data didn't include 'model'."}
    if not isinstance(model, str):
        return {"error": "'model' must be a string."}

    models = get_models()
    if (video_models := models.get("video-generation")) is None:
        return {"error": "There are currently no models available."}
    if model not in video_models:
        return {"error": f"'{model}' isn't an available model. {models}" }

    cfg = parse_config(VideoConfig, data)
    if isinstance(cfg, dict):
        return cfg

    model = model.replace("/", "--")
    start = time.time()
    base64 = generate_video(model, prompt, cfg)
    total = time.time() - start
    return {"duration": total, "base64": base64, "format" : "data:video/mp4;base64,"}

@app.route("/models")
def models():
    output = {}
    for model_type in [f for f in pathlib.Path("./models").glob("*") if f.is_dir()]:
        output[model_type.name] = [f.name.replace("--", "/") for f in model_type.iterdir() if f.is_dir()]
    return output

def parse_config(config: Type[Config], data: dict) -> dict | Config:
    cfg = config()
    if (config := data.get("config")) is not None:
        if not isinstance(config, dict):
            return {"error": "'config' must be a dictionary."}
        members = [attr for attr in dir(cfg) if not callable(getattr(cfg, attr)) and not attr.startswith("__")]
        for key, value in config.items():
            if key not in members:
                return {"error": f"Unexpected key: '{key}' in 'config'."}
            if not isinstance(value, type(getattr(cfg, key))):
                return {"error": f"Type '{type(value).__name__}' given, expected type '{type(getattr(cfg, key)).__name__}' of key '{key}' in 'config'"}
            setattr(cfg, key, value)
    return cfg



if __name__ == "__main__":

    if debug:
        app.run(debug=True, host="0.0.0.0", port=5000)
    else:
        serve(app, host="0.0.0.0", port=5000)
