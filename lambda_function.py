import boto3 #AWS SDK
import os #Allows write to path
import uuid
import traceback
from PIL import Image #pillow is an image proccesssing library
import PIL.Image
from resizeimage import resizeimage

THUMBNAIL_SIZE = [250,250]

def image_resize(image_source_path, resized_cover_path):
    with Image.open(image_source_path) as image:
        cover = resizeimage.resized_cover(image, THUMBNAIL_SIZE)
        cover.save(resized_cover_path, image.format)

#Handler function
#Writes to AWS S3 bucket
def handler(event, context):
    s3_client = boto3.client('s3')
    try:
        for record in event ['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            item_uuid=uuid.uuid4()
            os.mkdir('/tmp/{}'.format(item_uuid))
            download_path = '/tmp/{}/{}'.format(item_uuid, key)
            upload_path_thumbnail = '/tmp/resized-{}'.format(key)
            uploadToBucket = 'resizedimages'
            uploadFilename = 'resized/resized-'+key
            s3_client.download_file(bucket, key, download_path)
            image_resize(download_path, upload_path_thumbnail)
            s3_client.uploadfile(upload_path_thumbnail, uploadToBucket, uploadFilename)
    except Exception:
        print(traceback.format_exc())