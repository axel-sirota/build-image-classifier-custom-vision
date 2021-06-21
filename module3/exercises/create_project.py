import os

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry
from msrest.authentication import ApiKeyCredentials

os.chdir("../..")
# Replace with valid values
endpoint = os.environ["AZURE_CUSTOM_VISION_ENDPOINT"]
training_key = os.environ["AZURE_CUSTOM_VISION_SUBSCRIPTION_KEY"]

# Authenticate

# Create a new project

for root, dirs, files in os.walk("images", topdown=False):
    try:
        root_dir, category = root.split('/')
        if category != "Test":
            image_list = []
            tag_type = 'Regular' if category != 'Negative' else 'Negative'
            # Create tag for those images folder
            for image in files:
                if image != ".DS_Store":
                    print(f"Dealing with {category}/{image}")
                    with open(os.path.join(root_dir, category, image), "rb") as image_contents:
                        image_entry = None  # Create image entry
                        image_list.append(image_entry)
            print(f'Going to upload images from {category}')
            # Upload the images to project
    except ValueError:
        pass  # base directory

