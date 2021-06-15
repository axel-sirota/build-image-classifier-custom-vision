import os

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials

# Replace with valid values
os.chdir("..")
endpoint = os.environ["AZURE_COMPUTER_VISION_TRAINING_ENDPOINT"]
prediction_key = os.environ["AZURE_COMPUTER_VISION_TRAINING_SUBSCRIPTION_KEY"]

credentials = ApiKeyCredentials(in_headers={"Training-key": prediction_key})
trainer = CustomVisionTrainingClient(endpoint, credentials)
publish_iteration_name = "basic_waterfall_model"
project_name = f"waterfall_classification"
projects = trainer.get_projects()
for project in projects:
    if project.name == project_name:
        project_id = project.id

# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)

for root, dirs, files in os.walk("images/Test", topdown=False):
    for image in files:
        print(f"Dealing with {image}")
        with open(os.path.join(root, image), "rb") as image_contents:
            results = predictor.classify_image(project.id, publish_iteration_name, image_contents.read())

    # Display the results.
for prediction in results.predictions:
    print("\t" + prediction.tag_name +
          ": {0:.2f}%".format(prediction.probability * 100))
