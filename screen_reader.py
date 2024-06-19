from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv('AZURE_AI_KEY')
endpoint = "https://ergocrdev.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

read_response = computervision_client.read_in_stream(open("sample_erg_screen.jpeg", "rb"), raw=True)
read_operation_location = read_response.headers["Operation-Location"]
operation_id = read_operation_location.split("/")[-1]

while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break

results = [text_line.text for text in read_result.analyze_result.read_results for text_line in text.lines]
print(results)