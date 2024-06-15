import json
import numpy as np
from PIL import Image, ImageDraw
import os

def json_to_mask(json_file, output_path):
    with open(json_file) as f:
        data = json.load(f)
    
    images = {img['id']: img for img in data['images']}
    annotations = data['annotations']
    
    for annotation in annotations:
        if not annotation['segmentation']:  # Check if segmentation is empty
            print(f"No segmentation data for annotation ID {annotation['id']}")
            continue
        
        image_id = annotation['image_id']
        image_info = images[image_id]
        width, height = image_info['width'], image_info['height']
        
        mask = Image.new('RGB', (width, height), (0, 0, 0))  # Change mode to RGB
        
        # Debug print
        print(f"Processing annotation ID {annotation['id']} for image ID {image_id}")
        
        for seg in annotation['segmentation']:
            if len(seg) < 6:
                print(f"Invalid segmentation data for annotation ID {annotation['id']}")
                continue
            polygon = [(seg[i], seg[i + 1]) for i in range(0, len(seg), 2)]
            ImageDraw.Draw(mask).polygon(polygon, outline=(255, 255, 255), fill=(255, 255, 255))  # Change outline and fill to white
        
        output_file = os.path.join(output_path, image_info['file_name'].replace('.jpg', '.png'))  # Change file extension to .jpg
        mask.save(output_file)

# Paths to the directories
base_dir = 'dataset'
sub_dirs = ['train', 'valid', 'test']

for sub_dir in sub_dirs:
    json_dir = os.path.join(base_dir, sub_dir)
    output_dir = os.path.join(base_dir, sub_dir, 'masks')
    os.makedirs(output_dir, exist_ok=True)
    
    for json_file in os.listdir(json_dir):
        if json_file.endswith('.json'):
            json_path = os.path.join(json_dir, json_file)
            json_to_mask(json_path, output_dir)
