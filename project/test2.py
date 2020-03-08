import requests, json

subscription_key = '04cd658500e04aa4aa239fc5c96637ed'
assert subscription_key

face_api_url = 'https://comp3500-iot-azure-computer-vision.cognitiveservices.azure.com/face/v1.0/detect'

image_url = 'https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg'

headers= {'Ocp-Apim-Subscription-Key' : subscription_key}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accesories,blur,exposure,noise'}

response = requests.post(face_api_url, params=params,
                         headers=headers, json={"url": image_url})

print(json.dumps(response.json(), indent=2))
