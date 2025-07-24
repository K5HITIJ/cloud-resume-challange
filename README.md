# Cloud Resume Challenge

A cloud-based resume website with a visitor counter, built using AWS serverless technologies.

## Architecture

This project implements the Cloud Resume Challenge using the following AWS services:

- **Frontend**: Static website hosted on Amazon S3 with CloudFront CDN
- **Backend**: Serverless API using AWS Lambda and API Gateway
- **Database**: DynamoDB for storing visitor count
- **Infrastructure**: AWS SAM (Serverless Application Model) for Infrastructure as Code

## Project Structure

```
├── frontend/               # Static website files
│   ├── index.html         # Your resume HTML (empty - ready for your content)
│   ├── style.css          # Styling for the resume
│   └── script.js          # JavaScript for visitor counter
├── backend/               # Lambda function code
│   ├── app.py            # Main Lambda function
│   └── requirements.txt   # Python dependencies
├── infrastructure/        # AWS infrastructure
│   └── template.yaml     # SAM template
├── tests/                # Unit tests
│   └── test_app.py       # Lambda function tests
└── README.md             # This file
```

## Prerequisites

- AWS CLI installed and configured
- AWS SAM CLI installed
- Python 3.9+
- Node.js (for local testing)

## Deployment

1. **Build the SAM application:**
   ```bash
   sam build
   ```

2. **Deploy the infrastructure:**
   ```bash
   sam deploy --guided
   ```

3. **Upload frontend files to S3:**
   ```bash
   aws s3 sync frontend/ s3://your-bucket-name
   ```

## Local Development

1. **Start the SAM local API:**
   ```bash
   sam local start-api
   ```

2. **Run tests:**
   ```bash
   python -m pytest tests/
   ```

## Features

- ✅ Static resume website
- ✅ Visitor counter with real-time updates
- ✅ HTTPS enabled via CloudFront
- ✅ Serverless backend
- ✅ Infrastructure as Code
- ✅ Unit tests
- ✅ CI/CD ready

## Next Steps

1. Add your resume content to `frontend/index.html`
2. Customize the styling in `frontend/style.css`
3. Deploy the application using the commands above
4. Set up a custom domain (optional)
5. Implement CI/CD pipeline (optional)

## Security

- API Gateway configured with CORS
- DynamoDB with least privilege access
- CloudFront with security headers
- S3 bucket with public read-only access for website hosting
