from flask import Flask, render_template, request
import requests
import os
from datetime import datetime

app = Flask(__name__)
API_KEY = "ebd6cda7b840dae0bc53288e20b0babe9598ac4fbc759c7bd3653bd2e73643bf269a5970fac6489f45752d5bb6793e3e"
OUTPUT_FOLDER = "static/generated"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def generate_image(prompt, style):
    full_prompt = f"{prompt}, {style} style"
    url = "https://clipdrop-api.co/text-to-image/v1"

    try:
        print("📡 Sending request to ClipDrop...")
        response = requests.post(
            url,
            headers={
                "x-api-key": API_KEY,
                "Content-Type": "application/json"
            },
            json={"prompt": full_prompt}
        )

        print("🔍 Status:", response.status_code)
        if response.status_code == 200:
            filename = f"{style}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            filepath = os.path.join(OUTPUT_FOLDER, filename)
            with open(filepath, "wb") as f:
                f.write(response.content)
            return filepath
        else:
            print("❌ Error:", response.text)
            return None
    except Exception as e:
        print("❌ Exception:", str(e))
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    error = None

    if request.method == "POST":
        prompt = request.form["prompt"]
        style = request.form["style"]
        filepath = generate_image(prompt, style)
        if filepath:
            image_url = "/" + filepath.replace("\\", "/")
        else:
            error = "⚠️ Failed to generate image. Try again or check API."

    return render_template("index.html", image_url=image_url, error=error)

if __name__ == "__main__":
    app.run(debug=True)
