import requests
import json
from keras.preprocessing import image

img = image.img_to_array(image.load_img('../Dataset/building_minor/1. hurricane-sandy-flooded-apartment.jpg', target_size=(224,224))) / 255.
payload = {
  "instances": [{'input_image': img.tolist()}]
}
r = requests.post('http://localhost:9000/v1/models/DamageAnalyzer:predict', json=payload)
print(['building', 'minor', 'moderate', 'nodamage', 'severe', 'vehicle'])
print(json.loads(r.content.decode('utf-8')))
