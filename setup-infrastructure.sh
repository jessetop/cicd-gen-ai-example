#!/bin/bash

# Configuration
REGION="us-east-1"
CLUSTER_NAME="demo-cluster"
ECR_REPO="ai-chat-demo"
PIPELINE_NAME="ai-chat-pipeline"

echo "Setting up AWS infrastructure..."

# Create ECR repository
echo "Creating ECR repository..."
aws ecr create-repository --repository-name $ECR_REPO --region $REGION || echo "ECR repository already exists"

# Create EKS cluster (this takes 10-15 minutes)
echo "Creating EKS cluster..."
eksctl create cluster \
  --name $CLUSTER_NAME \
  --region $REGION \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed

# Update kubeconfig
echo "Updating kubeconfig..."
aws eks update-kubeconfig --region $REGION --name $CLUSTER_NAME

# Create namespace (optional)
kubectl create namespace ai-chat-demo || echo "Namespace already exists"

# Create secret for Hugging Face token (optional)
echo "Creating Kubernetes secret for Hugging Face token..."
echo "Please enter your Hugging Face token (or press Enter to skip):"
read -s HF_TOKEN
if [ ! -z "$HF_TOKEN" ]; then
  kubectl create secret generic ai-chat-secrets --from-literal=hugging-face-token=$HF_TOKEN
fi

echo "Infrastructure setup complete!"
echo "ECR Repository: $ECR_REPO"
echo "EKS Cluster: $CLUSTER_NAME"
echo "Region: $REGION"