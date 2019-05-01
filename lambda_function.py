import os
import boto3

def lambda_handler(event, context):

    client = boto3.client('ecs')

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_name_with_folder_prefix = event['Records'][0]['s3']['object']['key']
    object_name_no_folder_prefix = object_name_with_folder_prefix.split("/")[-1]

    input_video_path = "s3://" + bucket_name + "/" + object_name_with_folder_prefix
    output_video_name = "watermark-" + object_name_no_folder_prefix
    output_s3_bucket_name = bucket_name
    watermark_path = os.environ['WATERMARK_PATH']

    client.run_task(
        cluster=os.environ['CLUSTER'],
        taskDefinition=os.environ['TASK_DEFINITION'],
        count=int(os.environ['COUNT']),
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    os.environ['ECS_SUBNET_1'],
                    os.environ['ECS_SUBNET_2'],
                ],
                'securityGroups': [
                    os.environ['ECS_SECURITY_GROUP'],
                ],
                'assignPublicIp': 'ENABLED'
            }
        },
        overrides={
            'containerOverrides': [
                {
                    'name': os.environ['CONTAINER_NAME'],
                    'environment': [
                        {'name': 'INPUT_VIDEO_PATH','value': input_video_path},
                        {'name': 'OUTPUT_VIDEO_NAME','value': output_video_name},
                        {'name': 'OUTPUT_S3_BUCKET_NAME','value': output_s3_bucket_name},
                        {'name': 'WATERMARK_PATH','value': watermark_path}
                    ]
                }
            ]
        }
    )
