from flask import Flask, request, jsonify
from PIL import Image, ImageFilter, ImageOps
import numpy as np
# import cv2
import io
import base64


app = Flask(__name__)

# crop image
def crop_image(image,x,y,width,height):
    return image.crop((x, y, x + width, y + height))

#  compress image

def compress_image(image,quality=85):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=quality)
    return buffered.getvalue()

def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def apply_filter(image,filter_name):
    if filter_name == 'BLUR':
        return image.filter(ImageFilter.BLUR)
    elif filter_name == 'CONTOUR':
        return image.filter(ImageFilter.CONTOUR)
    elif filter_name == 'DETAIL':
        return image.filter(ImageFilter.DETAIL)
    elif filter_name == 'EDGE_ENHANCE':
        return image.filter(ImageFilter.EDGE_ENHANCE)
    elif filter_name == 'SHARPEN':
        return image.filter(ImageFilter.SHARPEN)
    else:
        return image

@app.route('/process-image', methods=['POST'])

def process_image():
    data = request.json
    image_data = base64.b64decode(data['image'])
    image = Image.open(io.BytesIO(image_data))
    operation = data['operation']
    if operation == 'crop':
        x, y, width, height = data['x'], data['y'], data['width'], data['height']
        processed_image = crop_image(image, x, y, width, height)
        img_str = image_to_base64(processed_image)
        return jsonify({'image': img_str})
    elif operation == 'compress':
        compressed_image_data = compress_image(image)
        img_str = base64.b64encode(compressed_image_data).decode('utf-8')
        return jsonify({'image': img_str})
    elif operation == 'filter':
         filter_name = data['filter_name']
         processed_image = apply_filter(image, filter_name)
    else:
        return jsonify({'error': 'Invalid operation'}), 400
    img_str = image_to_base64(processed_image)
    return jsonify({'image': img_str})
    

if __name__ == '__main__':
    app.run(debug=True)    