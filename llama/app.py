import os
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
import torch

token = os.environ.get("HF_TOKEN")
if token:
    login(token=token)
else:
    print("No HF_TOKEN found. Attempting to download public models only...")

app = Flask(__name__)

MODEL_NAMES = {
    "llama": "meta-llama/Llama-2-7b-hf",
    "gpt-neo": "EleutherAI/gpt-neo-2.7B",
    "gpt-j": "EleutherAI/gpt-j-6B"
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

models = {}
tokenizers = {}

for model_key, model_name in MODEL_NAMES.items():
    print(f"Loading {model_key} model on {device}...")
    tokenizers[model_key] = AutoTokenizer.from_pretrained(model_name)
    models[model_key] = AutoModelForCausalLM.from_pretrained(model_name).to(device)

@app.route("/generate", methods=["POST"])
def generate_text():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")
        model_key = data.get("model", "llama")
        max_length = data.get("max_length", 200)

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        if model_key not in models:
            return jsonify({"error": f"Model '{model_key}' not found"}), 400

        tokenizer = tokenizers[model_key]
        model = models[model_key]
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(inputs.input_ids, max_length=max_length, num_return_sequences=1)
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return jsonify({"status": f"Llama Multi-Model API is running on {device}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
