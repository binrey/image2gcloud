import os
import io
from PIL import Image

from google.cloud import storage

bucket_name = 'my_project_name.appspot.com'
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)

def upload_file(upload_file, file_name, new_width=500):
    """
    Upload file to the cloud storage
    Arguments: 
    upload_file -- binary file to be uploaded
    file_name -- name of file in clod storage
    new_width -- new width of uploaded files
    
    Returns:
    public_url -- http-path to stored file
    """

    blob = bucket.blob(file_name)
    pil_img = Image.open(upload_file)

    new_height = int(new_width/pil_img.size[0]*pil_img.size[1])
    pil_img = pil_img.resize((new_width, new_height))

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
