import requests, json

subscription_key = '11291157eba34c9c847b603363bc8def'
assert subscription_key

face_api_url = 'hhttps://comp3500-azure-face-api.cognitiveservices.azure.com/face/v1.0/detect'

image_url = 'https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg'

headers= {'Ocp-Apim-Subscription-Key' : subscription_key}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accesories,blur,exposure,noise'}

response = requests.post(face_api_url, params=params,
                         headers=headers, json={"url": image_url})

print(json.dumps(response.json(), indent=2))
