#!/bin/bash

aws s3 cp ${WATERMARK_PATH} watermark.png
aws s3 cp ${INPUT_VIDEO_PATH} input_video.mp4

ffmpeg -i input_video.mp4  -i watermark.png -filter_complex "overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2" ${OUTPUT_VIDEO_NAME}

aws s3 cp ${OUTPUT_VIDEO_NAME} s3://${OUTPUT_S3_BUCKET_NAME}/${OUTPUT_VIDEO_NAME}
