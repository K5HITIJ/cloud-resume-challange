#!/bin/bash

# Cloud Resume Challenge Deployment Script
# This script deploys the entire infrastructure and uploads the frontend

set -e

echo "🚀 Starting Cloud Resume Challenge deployment..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo "❌ SAM CLI is not installed. Please install it first."
    exit 1
fi

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials are not configured. Please run 'aws configure' first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Build the SAM application
echo "🔨 Building SAM application..."
sam build

# Deploy the SAM application
echo "🚀 Deploying SAM application..."
sam deploy --guided

# Get the outputs from the stack
echo "📋 Getting stack outputs..."
API_URL=$(aws cloudformation describe-stacks --stack-name cloud-resume-challenge --query "Stacks[0].Outputs[?OutputKey=='VisitorCounterApiUrl'].OutputValue" --output text)
BUCKET_NAME=$(aws cloudformation describe-stacks --stack-name cloud-resume-challenge --query "Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue" --output text)
CLOUDFRONT_URL=$(aws cloudformation describe-stacks --stack-name cloud-resume-challenge --query "Stacks[0].Outputs[?OutputKey=='CloudFrontURL'].OutputValue" --output text)

echo "✅ Stack deployed successfully!"
echo "📝 API URL: $API_URL"
echo "🪣 S3 Bucket: $BUCKET_NAME"
echo "🌐 CloudFront URL: $CLOUDFRONT_URL"

# Update the frontend JavaScript with the API endpoint
echo "🔧 Updating frontend with API endpoint..."
sed -i.bak "s|YOUR_API_GATEWAY_ENDPOINT|$API_URL|g" frontend/script.js
rm frontend/script.js.bak

# Upload frontend files to S3
echo "📤 Uploading frontend files to S3..."
aws s3 sync frontend/ s3://$BUCKET_NAME

echo "🎉 Deployment completed successfully!"
echo ""
echo "Your website is available at:"
echo "🌐 CloudFront URL: $CLOUDFRONT_URL"
echo ""
echo "Next steps:"
echo "1. Add your resume content to frontend/index.html"
echo "2. Test the visitor counter functionality"
echo "3. Consider setting up a custom domain"
