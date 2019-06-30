#!/bin/bash

# Options:
#   -x: Echo commands
#   -e: Fail on errors
#   -o pipefail: Fail on errors in scripts this calls, give stacktrace
set -ex -o pipefail

echo ${TRAVIS_PULL_REQUEST_BRANCH}

###########################
# Terraform deployment
###########################
deploy_terraform () {
  echo "  Deploying Terraform "
  if [[ ${TRAVIS_PULL_REQUEST_BRANCH} =~ 'azure' ]]; then
    cd infrastructure/azure/envs/stage
    terraform init -no-color
    terraform validate -no-color
    terraform plan -no-color
    terraform apply -no-color -auto-approve
  elif [[ ${TRAVIS_PULL_REQUEST_BRANCH} =~ 'gpc' ]]; then
    cd infrastructure/gcp/envs/stage
    terraform validate
    terraform plan -no-color
    terraform apply -no-color -auto-approve
  elif [[ ${TRAVIS_PULL_REQUEST_BRANCH} =~ 'aws' ]]; then
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
  echo "Testing the deployment"
  if [[ ${TRAVIS_PULL_REQUEST_BRANCH} =~ 'azure' ]]; then
    echo "Getting the Azure Kubeconfig"
    az aks get-credentials --resource-group kaos-2-stage-k8s --name kaos-2-stage-k8s
  elif [[ ${TRAVIS_PULL_REQUEST_BRANCH} =~ 'aws' ]]; then
    echo "Getting the AWS Kubeconfig"
    aws eks update-kubeconfig --name kaos-2-stage-eks-cluster --region eu-west-3
  fi
  NODES=$(kubectl get nodes)
  if [[ ${NODES} =~ "No resources found" ]] || [[ -z ${NODES} ]]; then
    echo "k8s Deployment Failed "
    exit 1
  else
    echo "k8s Deployment Passed "
  fi
}

source bootstrap.sh
deploy_terraform
test_k8s
