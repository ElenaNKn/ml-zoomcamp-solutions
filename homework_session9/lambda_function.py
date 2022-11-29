import urllib.request
import numpy as np
from io import BytesIO
from PIL import Image
import tflite_runtime.interpreter as tflite

interpreter = tflite.Interpreter(model_path='dino-dragon-model.tflite')
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']

def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img

def preprocess_image(x):
    x = np.true_divide(x, 255, dtype=np.float32)   
    return x

# url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Smaug_par_David_Demaret.jpg/1280px-Smaug_par_David_Demaret.jpg'

target_size = 150

def predict(url):
    
    img = download_image(url)
    img = prepare_image(img, (target_size, target_size))
    x = np.array(img, dtype='float32')
    X = np.array([x])
    X = preprocess_image(X)

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)
    
    return preds[0][0]


def lambda_handler(event, context):
    url = event['url']

    pred = predict(url)

    result = {'prediction' : pred}

    return result
