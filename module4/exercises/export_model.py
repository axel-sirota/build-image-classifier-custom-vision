import os
import time
import zipfile

import requests
from azure.cognitiveservices.vision.customvision.prediction.models import CustomVisionErrorException
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials


def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


# Do not worry about this function, it is for pretty printing the attributes!
def pretty_print(klass, indent=0):
    if '__dict__' in dir(klass):
        print(' ' * indent + type(klass).__name__ + ':')
        indent += 4
        for k, v in klass.__dict__.items():
            if '__dict__' in dir(v):
                pretty_print(v, indent)
            elif isinstance(v, list):
                print(' ' * indent + k + ':')
                for item in v:
                    pretty_print(item, indent)
            else:
                print(' ' * indent + k + ': ' + str(v))
    else:
        indent += 4
        print(' ' * indent + klass)


# Replace with valid values
os.chdir("../..")
endpoint = os.environ["AZURE_CUSTOM_VISION_ENDPOINT"]
training_key = os.environ["AZURE_CUSTOM_VISION_SUBSCRIPTION_KEY"]
prediction_resource_id = os.environ["AZURE_CUSTOM_VISION_RESOURCE_ID"]

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(endpoint, credentials)

project_name = f"waterfalls"
publish_iteration_name = "basic_waterfall_model"
project_id = None
projects = trainer.get_projects()
for project in projects:
    if project.name == project_name:
        project_id = project.id

if project_id is None:
    raise ValueError("Project does not exist")

# The iteration is now trained. Export it!
iterations = trainer.get_iterations(project_id=project_id)
# Export the iteration if it hasn't

exports = None   # Get the current exports, maybe sleep a bit before exporting above and this call

while len(exports) == 0:
    print("Waiting 10 seconds...")
    exports = None  # If it's still not done, refetch for updating
    time.sleep(10)

# Download the model export zip file and save it
