from flask import Flask, render_template
import os
from PIL import Image

app = Flask(__name__)

def create_thumbnail(image_path, thumbnail_path):
    size = (200, 200)
    image = Image.open(image_path)
    image.thumbnail(size)
    image.save(thumbnail_path)

@app.route('/')
def index():
    image_folder = os.path.join('static', 'images')
    thumbnail_folder = os.path.join('static', 'thumbnails')
    image_filenames = os.listdir(image_folder)
    
    for image_name in image_filenames:
        print(f"Processing image: {image_name}")
        image_path = os.path.join(image_folder, image_name)
        thumbnail_path = os.path.join(thumbnail_folder, image_name)
        if not os.path.exists(thumbnail_path):
            create_thumbnail(image_path, thumbnail_path)

    return render_template('index.html', images=image_filenames)

if __name__ == '__main__':
    app.run(debug=True)
