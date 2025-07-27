# ☁️ Cloud Resume Challenge

A simple serverless resume website with visitor counter, built using AWS services and automated CI/CD.

## 🏗️ Architecture

- **Frontend**: Static HTML website hosted on S3
- **Backend**: Lambda function with DynamoDB for visitor counting
- **API**: API Gateway REST endpoint
- **Infrastructure**: CloudFormation (Infrastructure as Code)
- **CI/CD**: GitHub Actions for automated deployment

## 🚀 Features

- ✅ Responsive resume website
- ✅ Real-time visitor counter
- ✅ Serverless architecture
- ✅ Automated deployments
- ✅ Infrastructure as Code

## 🔧 Setup

1. **Configure AWS Credentials**
   - Add `AWS_ACCESS_KEY_ID` to GitHub repository secrets
   - Add `AWS_SECRET_ACCESS_KEY` to GitHub repository secrets

2. **Deploy**
   - Push to `main` branch
   - GitHub Actions automatically deploys to AWS
   - Website URL will be displayed in the action logs

## 📁 Files

- `index.html` - Resume website
- `lambda_function.py` - Visitor counter backend
- `template.yaml` - AWS CloudFormation template
- `.github/workflows/deploy.yml` - CI/CD pipeline

## 🌐 Live Demo

Your website will be automatically deployed to: `http://cloud-resume-{account-id}.s3-website-us-east-1.amazonaws.com`

---

**Built for the Cloud Resume Challenge** 🎯

