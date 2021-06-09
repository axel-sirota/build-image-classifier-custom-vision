import os
from PIL import Image


def save_image(root, waterfall, filename):
    print(f"Dealing with {waterfall}/{filename}")
    if filename != ".DS_Store":
        if not os.path.exists(f'images/{waterfall}'):
            os.makedirs(f'images/{waterfall}')
        im1 = Image.open(f'{root}/{waterfall}/{filename}')
        im1.save(f'images/{waterfall}/{filename}', "JPEG", quality=25)


for root, dirs, files in os.walk("backups", topdown=False):
    try:
        root_dir, category = root.split('/')
        for image in files:
            save_image(root=root_dir, waterfall=category, filename=image)
    except ValueError:
        print(f"Error: {root}")