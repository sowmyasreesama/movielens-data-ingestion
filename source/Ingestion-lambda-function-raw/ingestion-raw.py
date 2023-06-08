import json
import os
import logging
from datetime import datetime
import boto3

logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s %(lineno)d %(levelname)s %(message)s",
)
log = logging.getLogger("Ingest-Raw")
log.setLevel(logging.INFO)


current_date = datetime.now() 
year = current_date.year
month = current_date.month
day = current_date.day
s3 = boto3.resource('s3')
s3_client=boto3.client('s3')
sns_client = boto3.client('sns')
code_bucket = os.environ['movielensconfig']



def lambda_handler(event, context):
    dataset=event.get("data_set") 
    
    response = s3_client.get_object(Bucket=code_bucket, Key=f"{dataset}/source_config/config.json")
    config_data = response.get('Body').read().decode('utf-8')
    config_json = json.loads(config_data)
    source_bucket = config_json.get('source-bucket')
    source_folder = config_json.get('source-folder')
    target_bucket = config_json.get('target-bucket')
    log.info(source_bucket)
 
    response = s3_client.list_objects_v2(Bucket=source_bucket)
 
   
 
    file_list = []
 
    for obj in response['Contents']:
        file_name = obj['Key']
        file_name = file_name.replace(source_folder + '/', '')
        file_list.append(file_name)
    log.info(file_list)

    for file in file_list[1:]:
        file_part = file.split('.')[0]
        file_extension = file.split('.')[1]
        log.info(file_part)
        otherkey = f"{dataset}/{file_part}/year={year}/month={month}/day={day}/{file_part}_{current_date}.{file_extension}"
        log.info(otherkey)
        copy_source = {
        'Bucket': source_bucket,
        'Key': f"{dataset}/{file}"
             
}
        bucket = s3.Bucket(target_bucket)
        bucket.copy(copy_source, otherkey)

    response = sns_client.publish(
    TopicArn='arn:aws:sns:us-east-1:118322642069:movielens',
    Message='Successfully Ingested Raw Data',
    Subject='Ingest Raw Data',)
    return {
        'statusCode': 200,
        'body': json.dumps('copy successful')
             
}