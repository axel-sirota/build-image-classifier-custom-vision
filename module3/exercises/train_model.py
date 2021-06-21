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
