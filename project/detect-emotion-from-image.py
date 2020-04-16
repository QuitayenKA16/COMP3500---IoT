import os, sys
import requests, json

# Variable required to access Azure Face API
subscription_key = '11291157eba34c9c847b603363bc8def'
face_api_url = 'https://comp3500-azure-face-api.cognitiveservices.azure.com/face/v1.0/detect'

if __name__ == '__main__':

    # Require console input: path of image to analyze
    if len(sys.argv) > 1:
        image_path = os.path.join(sys.argv[1])
    else:
        print("Usage: %s image_path" %s (sys.argv[0],))

    # Open image
    image_data = open(image_path, "rb")

    # headers and params for API post request
    headers= {'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key' : subscription_key}

    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'gender,emotion'
    }

    # Post reqest to Azure Face API
    response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
    
    # Store request response data into json file
    file = open("data.json", "w")
    file.write(response.text)
    file.close()
