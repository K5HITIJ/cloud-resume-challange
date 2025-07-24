#!/bin/bash

# Setup script for Cloud Resume Challenge development environment

echo "🛠️  Setting up Cloud Resume Challenge development environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or later."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✅ Python and pip are available"

# Install Python dependencies for testing
echo "📦 Installing Python test dependencies..."
pip3 install -r tests/requirements.txt

# Install runtime dependencies
echo "📦 Installing runtime dependencies..."
pip3 install -r backend/requirements.txt

echo "✅ Python dependencies installed"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "⚠️  AWS CLI is not installed. Please install it to deploy the project."
    echo "   Installation guide: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
else
    echo "✅ AWS CLI is available"
fi

# Check if SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo "⚠️  SAM CLI is not installed. Please install it to deploy the project."
    echo "   Installation guide: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html"
else
    echo "✅ SAM CLI is available"
fi

echo ""
echo "🎉 Setup complete! Next steps:"
echo ""
echo "1. Configure AWS credentials:"
echo "   aws configure"
echo ""
echo "2. Add your resume content to frontend/index.html"
echo ""
echo "3. Test the Lambda function locally:"
echo "   sam build && sam local start-api"
echo ""
echo "4. Deploy to AWS:"
echo "   ./deploy.sh"
echo ""
echo "5. Run tests:"
echo "   python -m pytest tests/ -v"
