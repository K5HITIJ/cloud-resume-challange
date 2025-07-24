<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Cloud Resume Challenge Project Instructions

This is a Cloud Resume Challenge project using AWS services:
- S3 for static website hosting
- CloudFront for CDN
- API Gateway + Lambda for visitor counter API
- DynamoDB for storing visitor count
- AWS SAM for Infrastructure as Code

## Project Structure
- `/frontend/` - Contains the static website files (HTML, CSS, JS)
- `/backend/` - Contains Lambda function code for the visitor counter
- `/infrastructure/` - Contains AWS SAM template for infrastructure
- `/tests/` - Contains unit tests

## Key Technologies
- Python for Lambda functions
- AWS SAM for deployment
- JavaScript for frontend visitor counter integration
- DynamoDB for data storage

When working on this project:
1. Use AWS best practices for security and performance
2. Follow serverless architecture patterns
3. Implement proper error handling and logging
4. Use environment variables for configuration
5. Write unit tests for Lambda functions
