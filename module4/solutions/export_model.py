import os
import time
import zipfile

import requests
from azure.cognitiveservices.vision.customvision.training.models._models_py3 import CustomVisionErrorException
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
print('Exporting Model Iteration...')
iterations = trainer.get_iterations(project_id=project_id)
try:
    trainer.export_iteration(project_id=project_id, iteration_id=iterations[0].id, platform='DockerFile', flavor='Linux')
except CustomVisionErrorException:
    print('Model is already ready for export')


exports = trainer.get_exports(project_id=project_id, iteration_id=iterations[0].id)
while exports[0].status == 'Exporting':
    exports = trainer.get_exports(project_id=project_id, iteration_id=iterations[0].id)
    print("Exporting. Waiting 10 seconds...")
    time.sleep(10)
print('Model export is found. Downloading...')
download_uri = exports[0].download_uri


download_url(url=download_uri, save_path='exported_model.zip')
os.makedirs('exported', exist_ok=True)
with zipfile.ZipFile("exported_model.zip", "r") as zip_ref:
    zip_ref.extractall("exported")
