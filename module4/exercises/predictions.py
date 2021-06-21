import operator
import os

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials

# Replace with valid values
os.chdir("../..")
endpoint = os.environ["AZURE_CUSTOM_VISION_ENDPOINT"]
prediction_key = os.environ["AZURE_CUSTOM_VISION_SUBSCRIPTION_KEY"]

credentials = ApiKeyCredentials(in_headers={"Training-key": prediction_key})
trainer = CustomVisionTrainingClient(endpoint, credentials)
publish_iteration_name = "basic_waterfall_model"
project_name = f"waterfalls"
projects = trainer.get_projects()
for project in projects:
    if project.name == project_name:
        project_id = project.id

# Now there is a trained endpoint that can be used to make a prediction. Authenticate for predictions
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)

for root, dirs, files in os.walk("images/Test", topdown=False):
    for image in files:
        print(f"Dealing with {image}")
        with open(os.path.join(root, image), "rb") as image_contents:
            results = None  # Get the prediction of the model
        predictions = {}
        # Populate the dict with the probability for each tag
        print(f'Prediction: {max(predictions.items(), key=operator.itemgetter(1))[0]}, Truth: {image}, Confidence: {max(predictions.items(), key=operator.itemgetter(1))[1] * 100} %')

