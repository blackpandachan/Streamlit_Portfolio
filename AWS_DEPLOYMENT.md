# AWS Deployment Guide for Portfolio App

This guide provides step-by-step instructions for deploying your Streamlit portfolio application to AWS with your custom domain, focusing on cost-effectiveness while maintaining scalability.

## Overview of Deployment Options

For a Streamlit portfolio site, there are several AWS deployment approaches:

1. **AWS Elastic Beanstalk** (Recommended): Simple deployment, auto-scaling, load balancing
2. **AWS App Runner**: Fully managed service for containerized applications
3. **AWS ECS (Fargate)**: Container orchestration with serverless compute
4. **AWS EC2**: Full control, but more maintenance overhead

This guide will focus primarily on AWS Elastic Beanstalk as it provides the best balance of simplicity, cost, and scalability for a portfolio site.

## Prerequisites

- AWS account
- AWS CLI installed and configured
- Docker installed locally
- Domain name (registered in Route 53 or transferable to Route 53)
- Basic familiarity with AWS services

## Option 1: AWS Elastic Beanstalk Deployment

### Step 1: Set Up AWS Environment

1. Install the EB CLI:
   ```bash
   pip install awsebcli
   ```

2. Configure AWS credentials:
   ```bash
   aws configure
   ```
   - Enter your AWS Access Key ID and Secret Access Key
   - Default region: Choose a region close to your target audience (e.g., `us-west-2`)
   - Default output format: `json`

### Step 2: Prepare Your Application for Deployment

1. Create an Elastic Beanstalk configuration file at `.elasticbeanstalk/config.yml`:
   ```yaml
   branch-defaults:
     main:
       environment: portfolio-prod
       group_suffix: null
   global:
     application_name: portfolio-app
     default_ec2_keyname: null
     default_platform: Docker
     default_region: us-west-2
     include_git_submodules: true
     instance_profile: null
     platform_name: null
     platform_version: null
     profile: null
     sc: git
     workspace_type: Application
   ```

2. Create a `Procfile` in your project root:
   ```
   web: streamlit run app.py --server.port=8080 --server.address=0.0.0.0
   ```

3. Create an `.ebignore` file to exclude unnecessary files:
   ```
   .git/
   .env
   __pycache__/
   *.pyc
   .elasticbeanstalk/*
   !.elasticbeanstalk/config.yml
   ```

4. If not already done, ensure your application handles API keys via environment variables or AWS Parameter Store.

### Step 3: Initialize Elastic Beanstalk Application

1. Initialize Elastic Beanstalk in your project directory:
   ```bash
   eb init portfolio-app --platform docker --region us-west-2
   ```

2. Create your environment:
   ```bash
   eb create portfolio-prod --instance-type t2.micro --single
   ```
   
   This creates a single instance environment with a t2.micro instance, which is eligible for the AWS Free Tier.

### Step 4: Environment Configuration

Configure environment variables:

1. From the AWS Console, go to Elastic Beanstalk > Environments > portfolio-prod
2. Click "Configuration" > "Software" > "Edit"
3. Under "Environment properties", add your variables:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `STREAMLIT_SERVER_PORT`: 8080
   - `STREAMLIT_SERVER_ADDRESS`: 0.0.0.0

### Step 5: Domain Configuration with Route 53

1. Register or transfer your domain to Route 53 (if not already done):
   - Go to Route 53 in the AWS Console
   - Click "Registered domains" > "Register domain" or "Transfer domain"
   - Follow the prompts to complete domain registration/transfer

2. Create a DNS record for your Elastic Beanstalk environment:
   - Go to Route 53 > Hosted zones
   - Select your domain
   - Click "Create record"
   - Set record type to "CNAME"
   - Set record name (e.g., "www" or leave blank for apex domain)
   - In the value field, enter your Elastic Beanstalk URL (e.g., `portfolio-prod.eba-abc123.us-west-2.elasticbeanstalk.com`)
   - Click "Create records"

3. For apex domain (e.g., example.com without www), use Route 53's Alias record:
   - Create a new record
   - Leave name field empty
   - Select "A - IPv4 address" as record type
   - Toggle "Alias" to "Yes"
   - Select "Alias to Elastic Beanstalk environment" and choose your environment
   - Click "Create records"

### Step 6: Set Up SSL Certificate with AWS Certificate Manager (ACM)

1. Request a certificate:
   - Go to AWS Certificate Manager
   - Click "Request a certificate" > "Request a public certificate"
   - Add domain names (both `example.com` and `www.example.com`)
   - Choose "DNS validation" and click "Request"

2. Validate the certificate:
   - If your domain is in Route 53, click "Create records in Route 53" to automatically add validation records
   - Otherwise, add the CNAME records to your DNS provider manually

3. Configure HTTPS for your Elastic Beanstalk environment:
   - Go to Elastic Beanstalk > Environments > portfolio-prod
   - Click "Configuration" > "Load balancer" > "Edit"
   - Under "Listeners", add a new listener with:
     - Port: 443
     - Protocol: HTTPS
     - SSL Certificate: Select your certificate
   - Click "Apply"

### Step 7: Cost Optimization

To keep costs low while maintaining scalability:

1. Use the AWS Free Tier:
   - t2.micro instances are included in the Free Tier for 12 months
   - 750 hours of EC2 usage per month (enough for one instance running 24/7)

2. Configure autoscaling:
   - Go to Elastic Beanstalk > Environments > portfolio-prod
   - Click "Configuration" > "Capacity" > "Edit"
   - Change "Environment Type" to "Load balanced"
   - Configure the scaling triggers:
     - Min instances: 1
     - Max instances: 2
     - Metric: CPUUtilization
     - Statistic: Average
     - Unit: Percent
     - Period: 5
     - Breach duration: 1
     - Upper threshold: 80
     - Scale up increment: 1
     - Lower threshold: 20
     - Scale down increment: -1
   - Click "Apply"

3. Set up application monitoring to track costs:
   - Go to AWS Budgets
   - Create a budget to alert you when costs approach a threshold

### Step 8: Automated Deployment with GitHub Actions

Create a GitHub workflow for continuous deployment in `.github/workflows/deploy-aws.yml`:

```yaml
name: Deploy to AWS

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install awsebcli
        
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-west-2
        
    - name: Deploy to Elastic Beanstalk
      run: |
        eb deploy portfolio-prod
```

To use this workflow:
1. Add your AWS credentials as secrets in your GitHub repository:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
2. Create an IAM user with the `AWSElasticBeanstalkFullAccess` policy

## Option 2: AWS App Runner Deployment

AWS App Runner is an alternative that requires even less configuration:

1. Build and push your Docker image to Amazon ECR:
   ```bash
   aws ecr create-repository --repository-name portfolio-app
   aws ecr get-login-password | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-west-2.amazonaws.com
   docker build -t portfolio-app .
   docker tag portfolio-app:latest $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-west-2.amazonaws.com/portfolio-app:latest
   docker push $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-west-2.amazonaws.com/portfolio-app:latest
   ```

2. Create App Runner service:
   - Go to AWS App Runner in the console
   - Click "Create service"
   - Select "Container registry" and "Amazon ECR"
   - Select your repository and image
   - Choose "Manual" deployment
   - Configure build: Port 8501, Environment variables for your API key
   - Service settings: Give your service a name, choose "Auto" for CPU/Memory
   - Click "Create & deploy"

3. Connect your domain:
   - In App Runner console, select your service
   - Go to "Custom domains" tab and click "Add domain"
   - Follow the prompts to validate and configure your domain

App Runner costs are typically higher than Elastic Beanstalk with a t2.micro instance but require less maintenance.

## Option 3: AWS Amplify Hosting (Experimental for Streamlit)

AWS Amplify can be an option, but requires additional configuration for Streamlit:

1. Create a `amplify.yml` configuration:
   ```yaml
   version: 1
   frontend:
     phases:
       build:
         commands:
           - echo "Building Streamlit app..."
           - pip install -r requirements.txt
     artifacts:
       baseDirectory: /
       files:
         - '**/*'
   ```

2. Create a custom `start.sh` script:
   ```bash
   #!/bin/bash
   streamlit run app.py --server.port=8080 --server.address=0.0.0.0
   ```

3. Deploy using Amplify Console:
   - Connect your GitHub repository
   - Configure build settings using the `amplify.yml` file
   - Add environment variables for your API key

This approach is experimental but might be viable for simple Streamlit apps. Consult AWS documentation for the latest compatibility information.

## Monitoring and Maintenance

1. Set up CloudWatch for monitoring:
   ```bash
   aws cloudwatch put-metric-alarm \
     --alarm-name portfolio-cpu-high \
     --alarm-description "Alarm when CPU exceeds 80%" \
     --metric-name CPUUtilization \
     --namespace AWS/EC2 \
     --statistic Average \
     --period 300 \
     --threshold 80 \
     --comparison-operator GreaterThanThreshold \
     --dimensions Name=AutoScalingGroupName,Value=portfolio-prod \
     --evaluation-periods 2 \
     --alarm-actions arn:aws:sns:us-west-2:123456789012:portfolio-alerts
   ```

2. Regular maintenance:
   - Update your application dependencies
   - Check AWS Health Dashboard for service notifications
   - Review security bulletins and update accordingly

## Troubleshooting

1. **Deployment failures**:
   - Check Elastic Beanstalk logs: `eb logs`
   - Check application logs in CloudWatch

2. **SSL certificate issues**:
   - Ensure your certificate is validated and in the same region as your EB environment
   - Check certificate status in ACM console

3. **Domain resolution problems**:
   - Verify DNS records in Route 53
   - Check that your domain is pointing to the correct EB URL

4. **Application errors**:
   - SSH into your instance: `eb ssh`
   - Check Docker logs: `docker logs $(docker ps -q)`

## Cost Estimates (2025)

| Service | Configuration | Estimated Monthly Cost |
|---------|---------------|------------------------|
| Elastic Beanstalk | t2.micro, 1 instance | $0 (Free Tier) or ~$8.50 |
| Route 53 | Domain + Hosted Zone | $0.50 + $12/year for domain |
| ACM | SSL Certificate | Free |
| CloudWatch | Basic monitoring | Free tier or ~$1-2 |
| **Total** | | **~$10-15/month** |

## Scaling Considerations

The setup described in this guide can easily scale to handle increased traffic:

1. **Vertical Scaling**: Change instance type from t2.micro to t2.small/medium
2. **Horizontal Scaling**: Increase max instances in auto-scaling group
3. **Content Delivery**: Add CloudFront for global content delivery
4. **Database**: Add DynamoDB or RDS if data storage requirements grow

## Security Best Practices

1. Store API keys in AWS Systems Manager Parameter Store:
   ```bash
   aws ssm put-parameter \
     --name "/portfolio/anthropic-api-key" \
     --type "SecureString" \
     --value "your-api-key"
   ```

2. Create a dedicated IAM role for your Elastic Beanstalk environment with minimal permissions

3. Enable AWS WAF for additional protection:
   - Go to AWS WAF in the console
   - Create a web ACL
   - Add rules to block common attack patterns
   - Associate with your Elastic Beanstalk environment

## Conclusion

This deployment approach provides a cost-effective, scalable solution for hosting your Streamlit portfolio application on AWS with a custom domain. The recommended Elastic Beanstalk configuration balances simplicity, cost, and future growth potential.

For any AWS-specific questions, refer to the [AWS Documentation](https://docs.aws.amazon.com/) or [AWS Support](https://aws.amazon.com/support/).
