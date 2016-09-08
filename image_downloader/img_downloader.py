from urllib import request
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

photo_count = 1

dst_path = os.path.join(BASE_DIR, 'media', 'photos')
os.makedirs(dst_path, exist_ok=True)

with open('photos.txt') as f:
    for line in f:
        dst_file = os.path.join(dst_path, str(photo_count) + '_extra.jpg')
        print('{2} of 534 Saving {0} to {1}'.format(line, dst_file, photo_count))
        request.urlretrieve(line, dst_file)
        photo_count += 1