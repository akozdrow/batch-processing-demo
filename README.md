# Overview

This is a detailed guide on how to create a video batch processing solution by leveraging S3, Lambda, and Fargate. 

When a user uploads a .mp4 video file to the designated S3 bucket, a Lambda function is triggered that runs a task in Fargate, which downloads the specified watermark from the S3 bucket and overlays it onto the video using ffmpeg. Once the video finishes processing, the Fargate task then uploads it back into the S3 bucket.

# Implementation Steps

### Create the Necessary IAM Roles with the Correct Policies Attached

### Create the ECS Cluster

1. Navigate to the ECS Section of the AWS Console and click "Clusters" in the sidebar.
2. Select the "Network only" cluster template which is powered by AWS Fargate
3. Give the cluster the name "batch-processing-cluster" and check the box that says to create a new VPC for the cluster. Ensure that at least two Subnets will be created within the VPC for high availability.
4. Click the create button. This will create the ECS Cluster along with a CloudFormation Stack that will take care of provisioning your VPC with the appropriate Security Groups, Route Table, Internet Gateway, etc.

### Create the ECS Task Definition

1. Click "Task Definitions" in the sidebar and then click on "Create new Task Definition".
2. Select Fargate as the desired launchtype and click "Next Steps".
3. Give your task definition the name "batch-processing-task".
4. Assign


