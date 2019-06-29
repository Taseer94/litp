#!/bin/bash

# Options:
#   -x: Echo commands
#   -e: Fail on errors
#   -o pipefail: Fail on errors in scripts this calls, give stacktrace
set -ex -o pipefail

echo ${TRAVIS_BRANCH}
echo ${TRAVIS_COMMIT_RANGE}

###########################
# Terraform Installation
###########################
echo "Installing Terraform"
sudo apt-get update
sudo apt-get install wget unzip apt-transport-https -y
wget https://releases.hashicorp.com/terraform/0.12.3/terraform_0.12.3_linux_amd64.zip
unzip terraform_0.12.3_linux_amd64.zip
sudo mv terraform /usr/local/bin
terraform -v

###########################
# Kubectl Installation
###########################
echo "Installing Kubectl"
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl

###########################
# AWS Installation
###########################
echo "Installing AWS CLI"
curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.13.7/2019-06-11/bin/linux/amd64/aws-iam-authenticator
chmod +x ./aws-iam-authenticator
mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$HOME/bin:$PATH
echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc

###########################
# Terraform deployment
###########################
if [[ ${TRAVIS_BRANCH} =~ "azure" ]]; then
  cd infrastructure/azure/envs/stage
  terraform init -no-color
  terraform validate -no-color
  terraform plan -no-color
  # terraform apply -no-color -auto-approve
elif [[ ${TRAVIS_BRANCH} =~ "gpc" ]]; then
  cd infrastructure/gcp/envs/stage
  terraform validate
  terraform plan -no-color
  # terraform apply -no-color -auto-approve
elif [[ ${TRAVIS_BRANCH} =~ "aws" ]]; then
  cd infrastructure/aws/envs/stage
  terraform validate
  terraform plan -no-color
  # terraform apply -no-color -auto-approve
fi

###########################
# K8s Tests
###########################
if [[ ${TRAVIS_BRANCH} =~ "master" ]]; then
  az aks get-credentials --resource-group kaos-2-stage-k8s --name kaos-2-stage-k8s
elif [[ ${TRAVIS_BRANCH} =~ "aws" ]]; then
  aws eks update-kubeconfig --name kaos-2-stage-eks-cluster --region eu-central-1
fi
NODES=$(kubectl get nodes)
if [[ "$NODES" =~ "No resources found" ]]; then
  echo "k8s Deployment Failed"
  exit 1
else
  echo "k8s Deployment Passed"
fi

###########################
# Pachyderm Test
###########################
pachctl create-repo images
pachctl put-file images master liberty.png -f http://imgur.com/46Q8nDz.png
pachctl list-repo
pachctl list-commit images
pachctl list-file images master
pachctl get-file images master liberty.png
pachctl create-pipeline -f https://raw.githubusercontent.com/pachyderm/pachyderm/master/examples/opencv/edges.json
sleep 5m
pachctl get-file edges master liberty.png
POD=$(kubectl get pods | grep pipeline)
if [[ "$POD" =~ "Running" ]]; then
  echo Pachyderm Deployment Successfull
else
  echo Pachyderm Deployment Failed
fi

