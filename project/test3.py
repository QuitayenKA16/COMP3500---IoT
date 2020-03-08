import asyncio
import glob, os, sys, time, uuid, requests

from urllib.parse import urlparse

from PIL import Image, ImageDraw
import io
from io import BytesIO

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

print ("done")
