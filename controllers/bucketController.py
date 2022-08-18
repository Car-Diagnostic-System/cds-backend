from flask import request, jsonify
import boto3
from werkzeug.utils import secure_filename
from datetime import datetime

s3 = boto3.resource(
        service_name='s3',
        region_name='ap-southeast-1',
        aws_access_key_id='AKIAS6J3LCRT4MC74Y75',
        aws_secret_access_key='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'
    )
BUCKET_NAME = 'cds-photo'
REGION = 's3.ap-southeast-1'

class BucketController:
    @staticmethod
    def uploadFile():
        # NOTE: request contain file
        CONTENT_TYPE = ['image/jpeg', 'image/png']
        try:
            file = request.files['file']
            if(not file):
                raise

            if file.content_type not in CONTENT_TYPE:
                return jsonify({'message': 'The file content type {} is not allowed'.format(file.content_type)}), 400

            file.filename = secure_filename('{0}-{1}'.format(datetime.now(), file.filename))
            bucket = s3.Bucket(BUCKET_NAME)
            bucket.upload_fileobj(file, Key=file.filename)
            url = f'https://{BUCKET_NAME}.{REGION}.amazonaws.com/{file.filename}'

            return jsonify(url)
        except:
            return jsonify({'message': 'The file is required'}), 400
