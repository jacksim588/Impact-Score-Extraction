from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from array import array
from PIL import Image
import os
import time


def ocr_image(image,subscription_key,endpoint):
    '''
    Authenticate
    Authenticates your credentials and creates a client.
    '''
    subscription_key = "8e547b16d3d04e9ba536e8a38fe6ad07"
    endpoint = "https://image-ocr-computer-vision.cognitiveservices.azure.com/"

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    '''
    END - Authenticate
    '''

    

    # Call API with URL and raw response (allows you to get the operation location)
    read_response = computervision_client.read_in_stream(image,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)
    out_text=''
    for line in read_result.analyze_result.read_results[0].lines:
        out_text=out_text+' '+line.text
    return(out_text)

