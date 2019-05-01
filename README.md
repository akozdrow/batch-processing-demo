# Overview

This is a detailed guide on how to create a video batch processing solution by leveraging S3, Lambda, and Fargate. 

When a user uploads a .mp4 video file to the designated S3 bucket, a Lambda function is triggered that runs a task in Fargate, which downloads the specified watermark from the S3 bucket and overlays it onto the video using ffmpeg. Once the video finishes processing, the Fargate task then uploads it back into the S3 bucket.

# Implementation Steps

### Configure the S3 Bucket

1. Create an S3 bucket with the default options selected. Assume that the name "video-batch-processing-bucket" is chosen and given to the bucket.
2. Within the newly created bucket, create two folders. Title one folder "unprocessed-vdeos" and title the other folder "watermarks". When a new .mp4 video 

### Create the Necessary IAM Roles with the Correct Policies Attached

##### IAM Role for ECS to access 

### Create the ECS Cluster

1. Navigate to the ECS Section of the AWS Console and click "Clusters" in the sidebar.
2. Select the "Network only" cluster template which is powered by AWS Fargate
3. Give the cluster the name "batch-processing-cluster" and check the box that says to create a new VPC for the cluster. Ensure that at least two Subnets will be created within the VPC for high availability.
4. Click the create button. This will create the ECS Cluster along with a CloudFormation Stack that will take care of provisioning your VPC with the appropriate Security Groups, Route Table, Internet Gateway, etc.

### Create the ECS Task Definition

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



