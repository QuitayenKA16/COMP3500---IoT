import json
import matplotlib.pyplot as plt
from matplotlib import patches
from PIL import Image
from io import BytesIO
import os

with open('data.json') as f:
    data = json.load(f)
    
print(json.dumps(data, indent=2))
print()
    
for d in data:
    print(d['faceId'])
    
image_path = os.path.join('people.jpeg')
image_read = open(image_path, "rb").read()
image = Image.open(BytesIO(image_read))

plt.figure(figsize=(8,8))
ax = plt.imshow(image, alpha=1)
for f in data:
    fr = f['faceRectangle']
    fa = f['faceAttributes']
    emotions = fa['emotion']
    highVal = 0
    highEmotion = 'anger'
    for e in emotions:
        if emotions[e] > highVal:
            highVal = emotions[e]
            highEmotion = e
    origin=(fr['left'], fr['top'])
    p = patches.Rectangle(
        origin, fr['width'], fr['height'], fill=False, linewidth=2, color='b')
    ax.axes.add_patch(p)
    plt.text(origin[0], origin[1], "%s" % (highEmotion),
             fontsize=10, color='b', va="bottom")

    
_ = plt.axis("off")
plt.show()
