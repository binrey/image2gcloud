import os
import io
from PIL import Image

from google.cloud import storage

bucket_name = 'my_project_name.appspot.com'
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)

NEW_WIDTH = 500

def upload_file(upload_file, file_name):
    """
    Upload file to the cloud storage
    Arguments: 
    upload_file -- binary file to be uploaded
    file_name -- name of file in clod storage

    Returns:
    public_url -- http-path to stored file
    """

    blob = bucket.blob(file_name)
    pil_img = Image.open(upload_file)

    NEW_HEIGHT = int(NEW_WIDTH/pil_img.size[0]*pil_img.size[1])
    pil_img = pil_img.resize((NEW_WIDTH, NEW_HEIGHT))

    b = io.BytesIO()
    pil_img.save(b, 'jpeg')
    pil_img.close()

    blob.upload_from_string(b.getvalue(), content_type='image/jpeg')
    
    blob.make_public()
    return blob.public_url

from urllib.request import urlopen
f = urlopen('https://look.com.ua/pic/201603/1920x1200/look.com.ua-154367.jpg')    
url = upload_file(f, 'puk.jpg')
print(url)
