from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image
import os
import base64
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('image_cropper.html')

@app.route('/crop', methods=['POST'])
def crop():
    app.logger.info(f"Received POST request: {request.form}")
    app.logger.info(f"Received files: {request.files}")

    try:
        # Get the JSON data containing cropped coordinates
        crop_data = request.json
        app.logger.info(f"Received crop request - Left: {crop_data['x']}, Top: {crop_data['y']}, Width: {crop_data['width']}, Height: {crop_data['height']}")

        # Decode base64 image data and create a PIL Image
        image_data = base64.b64decode(crop_data['dataUrl'].split(',')[1])
        image = Image.open(io.BytesIO(image_data))

        # Get cropping coordinates
        left = int(crop_data['x'])
        top = int(crop_data['y'])
        width = int(crop_data['width'])
        height = int(crop_data['height'])

        # Perform the crop
        cropped_img = image.crop((left, top, left + width, top + height))
        # Convert to RGB mode before saving as JPEG
        cropped_img = cropped_img.convert('RGB')

        # Get the directory of the current script (assuming app.py is in the root directory)
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Ensure the 'static' directory exists
        output_dir = os.path.join(script_dir, 'static')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_path = os.path.join(output_dir, 'cropped_image.jpg')
        cropped_img.save(output_path)

        return jsonify(success=True, message='Cropped image saved successfully')

    except Exception as e:
        app.logger.error(f"Error during crop: {e}")
        return jsonify(success=False, message=str(e))

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
    app.run(debug=True)
