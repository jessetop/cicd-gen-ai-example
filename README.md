# AI Chat Demo - GitHub Actions to CodePipeline to EKS

A Python Flask webapp that integrates with Hugging Face's free AI API, deployed via GitHub Actions to AWS EKS.

## Quick Setup (1 Hour)

### Prerequisites
- AWS CLI configured with appropriate permissions
- kubectl installed
- eksctl installed
- Docker installed (for local testing)
- GitHub repository with secrets configured

### Step 1: AWS Infrastructure Setup (15 minutes)
```bash
# Make script executable and run
chmod +x setup-infrastructure.sh
./setup-infrastructure.sh
```

### Step 2: Configure GitHub Secrets
Add these secrets to your GitHub repository:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### Step 3: Deploy Application (5 minutes)
```bash
# Push to main branch to trigger deployment
git add .
git commit -m "Initial deployment"
git push origin main
```

### Step 4: Access Application (5 minutes)
```bash
# Get the LoadBalancer URL
kubectl get service ai-chat-demo-service
```

## Local Development

### Run locally:
```bash
pip install -r requirements.txt
python app.py
```

### Build and test Docker image:
```bash
docker build -t ai-chat-demo .
docker run -p 5000:5000 ai-chat-demo
```

## Architecture

1. **GitHub Actions** builds and pushes Docker image to ECR
2. **AWS CodeBuild** (optional) can be integrated for additional build steps
3. **Amazon ECR** stores container images
4. **Amazon EKS** runs the containerized application
5. **LoadBalancer** exposes the application to the internet

## API Integration

Uses Hugging Face's free Inference API with DialoGPT model. No API key required for basic usage, but adding a token increases rate limits.

## Monitoring

- Health check endpoint: `/health`
- Kubernetes probes configured for liveness and readiness
- CloudWatch logs available through EKS

## Scaling

Adjust replicas in `k8s/deployment.yaml` or use:
```bash
kubectl scale deployment ai-chat-demo --replicas=5
```