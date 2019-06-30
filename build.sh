#!/bin/bash

# Options:
#   -x: Echo commands
#   -e: Fail on errors
#   -o pipefail: Fail on errors in scripts this calls, give stacktrace
set -ex -o pipefail

###########################
# Terraform Installation
###########################
install_terraform () {
  echo "----------------------"
  echo " Installing Terraform "
  echo "----------------------"
  sudo apt-get update
  sudo apt-get install wget unzip apt-transport-https jq -y
  wget https://releases.hashicorp.com/terraform/0.12.3/terraform_0.12.3_linux_amd64.zip
  unzip terraform_0.12.3_linux_amd64.zip
  sudo mv terraform /usr/local/bin
  terraform -v
}

###########################
# Kubectl Installation
###########################
install_kubectl() {
  echo "----------------------"
  echo "  Installing Kubectl  "
  echo "----------------------"
  curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
  chmod +x ./kubectl
  sudo mv ./kubectl /usr/local/bin/kubectl
}

###########################
# Terraform deployment
###########################
deploy_terraform () {
  echo "----------------------"
  echo "  Deploying Terraform "
  echo "----------------------"
  if [[ ${TRAVIS_BRANCH} =~ 'azure' ]]; then
    cd infrastructure/azure/envs/stage
    terraform init -no-color
    terraform validate -no-color
    terraform plan -no-color
    terraform apply -no-color -auto-approve
  elif [[ ${TRAVIS_BRANCH} =~ 'gpc' ]]; then
    cd infrastructure/gcp/envs/stage
    terraform validate
    terraform plan -no-color
    terraform apply -no-color -auto-approve
  elif [[ ${TRAVIS_BRANCH} =~ 'aws' ]]; then
    cd infrastructure/aws/envs/stage
    terraform validate
    terraform plan -no-color
    terraform apply -no-color -auto-approve
  fi
}

###########################
# K8s Tests
###########################
test_k8s () {
  echo "----------------------"
  echo "Testing the deployment"
  echo "----------------------"
  if [[ ${TRAVIS_BRANCH} =~ 'azure' ]]; then
    az aks get-credentials --resource-group kaos-2-stage-k8s --name kaos-2-stage-k8s
  elif [[ ${TRAVIS_BRANCH} =~ 'aws' ]]; then
    echo "----------------------"
    echo "  Installing AWS CLI  "
    echo "----------------------"
    curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.13.7/2019-06-11/bin/linux/amd64/aws-iam-authenticator
    chmod +x ./aws-iam-authenticator
    mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$HOME/bin:$PATH
    echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc

    echo "----------------------"
    echo "Getting the Kubeconfig"
    echo "----------------------"
    aws eks update-kubeconfig --name kaos-2-stage-eks-cluster --region eu-west-3
  fi
  NODES=$(kubectl get nodes)
  if [[ ${NODES} =~ "No resources found" ]] || [[ -z ${NODES} ]]; then
    echo "----------------------"
    echo "k8s Deployment Failed "
    echo "----------------------"
    exit 1
  else
    echo "----------------------"
    echo "k8s Deployment Passed "
    echo "----------------------"
  fi
}


source bootstrap.sh
