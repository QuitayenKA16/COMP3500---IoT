import os, sys
import requests, json
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import patches
from io import BytesIO

subscription_key = '11291157eba34c9c847b603363bc8def'
face_api_url = 'https://comp3500-azure-face-api.cognitiveservices.azure.com/face/v1.0/detect'

emotions = ['anger', 'contempt', 'digust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']

if __name__ == '__main__':

    if len(sys.argv) > 1:
        image_path = os.path.join(sys.argv[1])
    else:
        print("Usage: %s image_path" %s (sys.argv[0],))

    image_data = open(image_path, "rb")

    headers= {'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key' : subscription_key}

    faceAttributesList = 'gender,emotion'

    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': faceAttributesList
    }

    response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
    print(json.dumps(response.json(), indent=2))
    file = open("data.txt", "w")
    file.write(response.text)
    file.close()
