import os
import time

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials

# Replace with valid values
os.chdir("../..")
endpoint = os.environ["AZURE_CUSTOM_VISION_ENDPOINT"]
training_key = os.environ["AZURE_CUSTOM_VISION_SUBSCRIPTION_KEY"]
prediction_resource_id = os.environ["AZURE_CUSTOM_VISION_RESOURCE_ID"]

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(endpoint, credentials)

project_name = f"waterfalls"

projects = trainer.get_projects()
for project in projects:
    if project.name == project_name:
        project_id = project.id

print ("Training...")
iteration = trainer.train_project(project_id, force_train=True)
time.sleep(30)
while iteration.status != "Completed":
    iteration = trainer.get_iteration(project.id, iteration.id)
    print("Training status: " + iteration.status)
    print("Waiting 10 seconds...")
    time.sleep(10)
