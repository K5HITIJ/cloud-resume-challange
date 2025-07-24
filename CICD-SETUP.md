# CI/CD Configuration

## AWS Resources for CI/CD

### SAM Deployment Bucket
- **Bucket Name**: `cloud-resume-sam-deployments-1753354685`
- **Purpose**: Stores SAM deployment artifacts
- **Region**: us-east-1

### GitHub Secrets Required

```
AWS_ACCESS_KEY_ID=your_iam_user_access_key
AWS_SECRET_ACCESS_KEY=your_iam_user_secret_key
SAM_S3_BUCKET=cloud-resume-sam-deployments-1753354685
CLOUDFRONT_DOMAIN=dlwihg4xkk5ga.cloudfront.net
```

### Environment Configuration

#### Staging Environment
- Stack Name: `cloud-resume-staging`
- S3 Bucket: `cloud-resume-staging-bucket`
- DynamoDB Table: `VisitorCounter-staging`

#### Production Environment
- Stack Name: `cloud-resume-challenge`
- S3 Bucket: `cloud-resume-challenge-bucket`
- DynamoDB Table: `VisitorCounter`
- CloudFront URL: https://dlwihg4xkk5ga.cloudfront.net

## Setup Instructions

1. **Create GitHub Repository**
   ```bash
   git add .
   git commit -m "feat: implement CI/CD pipeline with staging/production environments"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Configure GitHub Secrets**
   - Go to your GitHub repository
   - Settings → Secrets and variables → Actions
   - Add the secrets listed above

3. **Create GitHub Environments**
   - Settings → Environments
   - Create `staging` environment
   - Create `production` environment (with protection rules)

4. **First Deployment**
   - Push to main branch
   - Watch GitHub Actions run your pipeline
   - Verify staging deployment
   - Approve production deployment

## Pipeline Benefits

✅ **Professional DevOps Practices**
- Multi-environment deployment strategy
- Automated testing at every stage
- Infrastructure as Code with SAM
- Security-first approach

✅ **Quality Assurance**
- Unit tests prevent broken code
- Integration tests ensure API functionality
- Linting maintains code quality
- Performance testing catches regressions

✅ **Production Readiness**
- Staging environment for safe testing
- Automated rollback capabilities
- CloudFront cache management
- Environment-specific configurations

✅ **Employer Appeal**
- Demonstrates CI/CD expertise
- Shows testing best practices
- Proves automation skills
- Exhibits production mindset
