import boto3
import logging

# 创建 S3 客户端
s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIAUL3M5JWSXJWM5RRE',
    aws_secret_access_key='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',
    region_name='ap-southeast-1'
)

# 您的字节流数据
data_bytes = b"This is a test byte stream."

# 上传字节流到 S3 存储桶中的文件
bucket_name = 'nft-erm-bucket'  # 替换为您的 S3 存储桶名称
expiration_time = 3600  # URL 的过期时间，单位为秒


def upload_file(file_name, data_bytes):
    try:
        res = s3_client.put_object(Body=data_bytes, Bucket=bucket_name, Key=file_name)
        return res
    except Exception as e:
        logging.exception(e)
        return False


def get_file_url(file_name):
    try:
        # 生成预签名 URL
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket_name, 'Key': file_name},
            ExpiresIn=expiration_time,
        )
        return url
    except Exception as e:
        logging.exception(e)
        return None


def download_file(file_name):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        file_content = response['Body'].read()  # 获取字节流内容
        return file_content
    except Exception as e:
        logging.exception(e)
        return None

