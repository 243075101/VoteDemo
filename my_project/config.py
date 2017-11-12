import os

port = 8000

BASE_DIR = os.path.dirname(__file__)

app_seting = {

    'debug':True,
    'static_path':os.path.join(BASE_DIR,'static'),
    'template_path':os.path.join(BASE_DIR,'templates')
}

