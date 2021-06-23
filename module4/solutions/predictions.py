import operator
import os

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
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
            results = predictor.classify_image(project.id, publish_iteration_name, image_contents.read())
        predictions = {}
        for prediction in results.predictions:
            predictions[prediction.tag_name] = prediction.probability
        print(f'Prediction: {max(predictions.items(), key=operator.itemgetter(1))[0]}, Truth: {image}, Confidence: {max(predictions.items(), key=operator.itemgetter(1))[1] * 100} %')
