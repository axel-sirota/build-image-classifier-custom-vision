import os
import time

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials


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
