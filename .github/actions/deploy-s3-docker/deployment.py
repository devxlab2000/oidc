import os
import mimetypes
import boto3
from botocore.config import Config


def run():
    bucket = os.environ['INPUT_BUCKET']
    bucket_region = os.environ['INPUT_BUCKET-REGION']
    dist_folder = os.environ['INPUT_DIST-FOLDER']

    configuration = Config(region_name=bucket_region)

    s3_client = boto3.client('s3', config=configuration)

    for root, subdirs, files in os.walk(dist_folder):
        for file in files:
            file_path = os.path.join(root, file)
            key = os.path.relpath(file_path, dist_folder).replace(os.sep, '/')
            content_type = mimetypes.guess_type(file)[0] or 'application/octet-stream'
            s3_client.upload_file(file_path, bucket, key, ExtraArgs={'ContentType': content_type})

    website_url = f'http://{bucket}.s3-website-{bucket_region}.amazonaws.com'
    print(f'::set-output name=website-url::{website_url}')


if __name__ == '__main__':
    run()
