from flask import Flask, render_template, send_from_directory, request, jsonify
import os
from PIL import Image
import json

app = Flask(__name__)

def create_thumbnail(image_path, thumbnail_path):
    size = (200, 200)
    image = Image.open(image_path)
    image.thumbnail(size)
    image.save(thumbnail_path)

def load_tags():
    try:
        with open("tags.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_tags(tags):
    with open("tags.json", "w") as file:
        json.dump(tags, file)

predefined_tags = ['tag1', 'tag2', 'tag3']  # You can replace these with your own predefined tags

@app.route('/')
def index():
    image_folder = os.path.join('static', 'images')
    thumbnail_folder = os.path.join('static', 'thumbnails')
    image_filenames = os.listdir(image_folder)

    hardcoded_tags = ["tag1", "tag2", "tag3"]
    saved_tags = load_tags()
    
    for image_name in image_filenames:
        # print(f"Processing image: {image_name}")
        image_path = os.path.join(image_folder, image_name)
        thumbnail_path = os.path.join(thumbnail_folder, image_name)
        if not os.path.exists(thumbnail_path):
            create_thumbnail(image_path, thumbnail_path)

    hardcoded_tags = ["tag1", "tag2", "tag3"]
    return render_template('index.html', images=image_filenames, tags=hardcoded_tags, saved_tags=saved_tags)

@app.route('/save_tags', methods=['POST'])
def save_tags_route():
    tags_data = json.loads(request.form['tags'])
    all_tags = load_tags()

    for image, tag in tags_data.items():
        all_tags[image] = tag

    save_tags(all_tags)

    return {"message": "Tags saved."}

@app.route('/delete_tags', methods=['POST'])
def delete_tags_route():
    image = request.form['image']

    all_tags = load_tags()
    if image in all_tags:
        del all_tags[image]
        save_tags(all_tags)

    return {"message": "Tags deleted."}

if __name__ == '__main__':
    app.run(debug=True)