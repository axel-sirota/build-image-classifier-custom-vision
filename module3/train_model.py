import os
import time

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials

# Replace with valid values
os.chdir("..")
endpoint = os.environ["AZURE_COMPUTER_VISION_TRAINING_ENDPOINT"]
training_key = os.environ["AZURE_COMPUTER_VISION_TRAINING_SUBSCRIPTION_KEY"]
prediction_resource_id = os.environ["AZURE_COMPUTER_VISION_TRAINING_RESOURCE_ID"]

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(endpoint, credentials)

project_name = f"definitive_waterfalls"
publish_iteration_name = "basic_waterfall_model"

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

# The iteration is now trained. Publish it to the project endpoint
iterations = trainer.get_iterations(project_id=project.id)
trainer.publish_iteration(project.id, iterations[-1].id, publish_iteration_name, prediction_resource_id)
print("Done!")
