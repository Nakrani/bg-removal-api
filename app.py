from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "BG Removal API Ready!"})

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "Image required"}), 400
        file = request.files['image']
        img = Image.open(file.stream)
        result = remove(img)
        output = io.BytesIO()
        result.save(output, format='PNG')
        output.seek(0)
        return send_file(output, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
