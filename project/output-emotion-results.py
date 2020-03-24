import json
import matplotlib.pyplot as plt
from matplotlib import patches
from PIL import Image
from io import BytesIO
import os, sys

with open('data.json') as f:
    data = json.load(f)
    
print(json.dumps(data, indent=2))
print()


#for d in data:
#    print(d['faceId'])

image_path = os.path.join(sys.argv[1])
image_read = open(image_path, "rb").read()
image = Image.open(BytesIO(image_read))

plt.figure(figsize=(8,8))
ax = plt.imshow(image, alpha=1)
for f in data:
    fr = f['faceRectangle']
    fa = f['faceAttributes']
    emotions = fa['emotion']
    origin=(fr['left'], fr['top'])
    p = patches.Rectangle(origin, fr['width'], fr['height'], fill=False, linewidth=2, color='b')
    ax.axes.add_patch(p)

    highVal = 0
    highEmotion = 'anger'
    yVal = origin[1];
    for e in emotions:
        plt.text(origin[0]+fr['width']+5, yVal, "%s: %s" % (e, emotions[e]), fontsize=10, color='y', va="top")
        yVal += 40
        if emotions[e] > highVal:
            highVal = emotions[e]
            highEmotion = e
    plt.text(origin[0], origin[1], "%s" % (highEmotion),fontsize=12, color='b', va="bottom")

    
_ = plt.axis("off")
plt.show()
