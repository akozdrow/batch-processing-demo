# Overview

This is a detailed guide on how to create a video batch processing solution by leveraging S3, Lambda, and Fargate. 

When a user uploads a [.mp4 video file](https://raw.githubusercontent.com/akozdrow/batch-processing-demo/master/test-video.mp4) to the designated S3 bucket, a Lambda function is triggered that runs a task in Fargate, which downloads the specified watermark from the S3 bucket and overlays it onto the video using ffmpeg. Once the video finishes processing, the Fargate task then uploads the [processed video with the overlayed watermark](https://raw.githubusercontent.com/akozdrow/batch-processing-demo/master/watermark-test-video.mp4) back into the S3 bucket.

# Implementation Steps

### I. Configure the S3 Bucket

1. Navigate to the S3 section of the AWS console.
2. Create an S3 bucket with the default options selected. Assume that the name "video-batch-processing-bucket" is chosen and given to the bucket.
3. Within the newly created bucket, create two folders. Title one folder "unprocessed-vdeos" and title the other folder "watermarks". *CONTEXT:* When a new .mp4 video is uploaded into the unprocessed-videos folder, this will trigger an event (the event will be configured in the Lambda section) that kicks off the video watermarking process. The watermarks folder is a place to store various watermarks which can be applied onto uploaded videos. Processed videos will be reuploaded directly into the bucket and will not sit within any folder.

### II. Create the Necessary IAM Roles with the Correct Policies Attached

##### IAM Role for an ECS task to access S3

1. Navigate to the Identity and Access Management section of the AWS console and click "Roles" on the sidebar.
2. Click "Create Role" and choose "Elastic Container Service" for the service that will use your role.
3. Select "Elastic Container Service Task" for your use case.
4. Click "Next:Permissions", click "Create Policy", and click on the "JSON" tab.
5. Copy and paste the [following permissions policy](https://raw.githubusercontent.com/akozdrow/batch-processing-demo/master/ecsS3Access.json), and make sure that within the policy all references to "video-batch-processing-bucket" are replaced by the name of your own bucket. Click "Review policy".
6. Give the policy a name of "ecsS3Access", give it a description, and click "Create policy".
7. Back to where the role is being created, search for the newly created ecsS3Access permissions policy and attach it to the role by clicking the checkbox next to the policy name.
8. Skip through adding any tags.
9. Give the role the name "ecsS3TaskRole" and click "Create role".

##### IAM Role for Lambda functions to trigger ECS tasks

1. Navigate to the Identity and Access Management section of the AWS console and click "Roles" on the sidebar.
2. Click "Create Role" and choose "Lambda" for the service that will use your role.
3. Click "Next:Permissions", click "Create Policy", and click on the "JSON" tab
4. Copy and paste the [following permissions policy](https://raw.githubusercontent.com/akozdrow/batch-processing-demo/master/ecsRunTask.json).
5. Give the policy a name of "ecsRunTask", give it a description, and click "Create policy".
6. Back to where the role is being created, search for the newly created ecsRunTask permissions policy and attach it to the role by clicking the checkbox next to the policy name.
7. Search for the "AWSLambdaBasicExecutionRole" policy and attach it to the role as well by clicking the checkbox next to the policy name.
8. Skip through adding any tags.
9. Give the role the name "lambdaExecutionRole" and click "Create role".


### III. Create and Configure the Lambda Function

### IV. Create the ECS Cluster

1. Navigate to the ECS Section of the AWS console and click "Clusters" in the sidebar.
2. Select the "Network only" cluster template which is powered by AWS Fargate
3. Give the cluster the name "batch-processing-cluster" and check the box that says to create a new VPC for the cluster. Ensure that at least two Subnets will be created within the VPC for high availability.
4. Click the create button. *CONTEXT:* This will create the ECS Cluster along with a CloudFormation Stack that will take care of provisioning your VPC with the appropriate Security Groups, Route Table, Internet Gateway, etc.

### V. Create the ECS Task Definition

1. Click "Task Definitions" in the sidebar and then click on "Create new Task Definition".
2. Select Fargate as the desired launchtype and click "Next Steps".
3. Give your task definition the name "batch-processing-task".
4. Assign the "ecsS3TaskRole" to the task which was created in the previous steps.
5. Ensure that awsvpc is selected for the Network Mode.
6. Ensure that a task execution role will be created for you if you do not already have one.
7. Assign 0.5GB of memory and 0.25 vCPU to the task.
8. Click the "Add Container" button and give it the name of "batch-processing-container"
9. For the container image, either use "akozdrow/aws:latest", which will pull from [Dockerhub](https://cloud.docker.com/u/akozdrow/repository/docker/akozdrow/aws), or specify your own path two wherever your container is stored.
10. Keep everything else as is and click "Add".

### VI. Test Out the Implementation



