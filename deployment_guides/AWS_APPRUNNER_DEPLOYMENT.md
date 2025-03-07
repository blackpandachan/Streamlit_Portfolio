# AWS App Runner Deployment Guide for Portfolio App

This comprehensive guide will walk you through deploying your Streamlit portfolio application using AWS App Runner - a fully managed service that makes it easy to deploy containerized web applications and APIs.

## Why App Runner?

AWS App Runner offers several advantages for portfolio applications:

- **Fully managed infrastructure** - no need to provision or manage servers
- **Automatic scaling** based on traffic
- **Cost-effective** with pay-for-what-you-use pricing
- **Built-in CI/CD** with direct GitHub integration
- **Simplified deployment** with minimal configuration
- **Automatic HTTPS** and load balancing
- **Easy custom domain configuration** with Route 53

## Prerequisites

- AWS account
- GitHub account with your portfolio repository
- Domain registered in Route 53 (optional, for custom domain)
- Docker installed locally (for testing container builds)

## Step 1: Prepare Your Application

Ensure your portfolio application is properly containerized:

1. **Verify your Dockerfile**
   ```Dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Add an `apprunner.yaml` file** to your repository root (optional but recommended):
   ```yaml
   version: 1.0
   runtime: python3
   build:
     commands:
       build:
         - pip install -r requirements.txt
   run:
     command: streamlit run app.py --server.port=8501 --server.address=0.0.0.0
     network:
       port: 8501
       env: APP_PORT
   ```

3. **Test your container locally**:
   ```bash
   docker build -t portfolio-app .
   docker run -p 8501:8501 portfolio-app
   ```
   Visit `http://localhost:8501` to verify it works.

## Step 2: Deploy with App Runner Console

### Option A: Deploy from Source Code (GitHub)

1. **Sign in to AWS Console** and navigate to App Runner service

2. **Create a new service**:
   - Click "Create service"
   - Select "Source code repository"
   - Click "Add new" to connect your GitHub account
   - Authorize AWS App Runner to access your GitHub repositories
   - Select your portfolio repository and branch (e.g., `main`)

3. **Configure build**:
   - Select "Configure all settings here"
   - Runtime: Python 3
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --server.port=8501 --server.address=0.0.0.0`
   - Port: `8501`

4. **Configure service**:
   - Service name: `portfolio-app`
   - CPU: 1 vCPU
   - Memory: 2 GB (can be adjusted based on needs)
   - Environment variables:
     - Add `ANTHROPIC_API_KEY` with your API key value
     - Add any other required environment variables

5. **Configure auto scaling**:
   - Concurrent requests per instance: 100 (default is fine)
   - Min instances: 1
   - Max instances: 2 (adjust as needed)

6. **Click "Create & deploy"**

### Option B: Deploy from Container Registry (ECR)

1. **Build and push your Docker image to Amazon ECR**:
   ```bash
   # Create repository
   aws ecr create-repository --repository-name portfolio-app
   
   # Login to ECR
   aws ecr get-login-password | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com
   
   # Build image
   docker build -t portfolio-app .
   
   # Tag image
   docker tag portfolio-app:latest $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com/portfolio-app:latest
   
   # Push image
   docker push $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com/portfolio-app:latest
   ```

2. **Create App Runner service from ECR image**:
   - In App Runner console, click "Create service"
   - Select "Container registry"
   - Select "Amazon ECR" as the registry type
   - Select your repository and image
   - Set deployment to "Manual"
   - Configure service settings as described in Option A

## Step 3: Configure Custom Domain

1. **Add a custom domain to your App Runner service**:
   - In the App Runner console, select your service
   - Navigate to the "Custom domains" tab
   - Click "Add domain"
   - Enter your domain name (e.g., `portfolio.example.com`)
   - Click "Add"

2. **Verify domain ownership**:
   - App Runner will display DNS records needed for verification
   - Go to Route 53 console (or your DNS provider)
   - Add the CNAME records provided by App Runner
   - Return to App Runner and wait for verification to complete

3. **Create DNS records for your domain**:
   - Once verified, App Runner provides the DNS target for your service
   - Go to Route 53 and create a CNAME record pointing to this target:
     - Record name: `portfolio` (or subdomain of choice)
     - Record type: CNAME
     - Value: (App Runner domain provided, e.g., `jk5yu7jk7f.us-east-1.awsapprunner.com`)
     - TTL: 300 seconds

4. **Set up SSL certificate**:
   - App Runner automatically provisions an SSL certificate for your domain
   - This process can take 30-40 minutes to complete
   - Once done, your domain will show "Active" status in App Runner

## Step 4: Setting Up GitHub Integration for CI/CD

The GitHub integration with App Runner provides automatic deployments when you push code changes.

### Configure Automatic Deployments

1. **In the App Runner console**:
   - Select your service
   - Click on "Configuration" tab
   - Click "Edit" in the "Source and deployment" section
   - Under "Deployment settings", select "Automatic" 
   - Choose the branches to trigger deployments (usually `main`)
   - Save changes

2. **Understanding deployment triggers**:
   - Push to the configured branch automatically starts a new deployment
   - App Runner checks for changes in source code
   - Build and deployment logs are available in the console
   - Deployment history is maintained for rollback if needed

### GitHub Repository Configuration Best Practices

1. **Branch protection rules**:
   - Enable branch protection for your deployment branch
   - Require pull request reviews before merging
   - Require status checks to pass before merging

2. **Repository secrets**:
   - Don't store sensitive information in your code
   - Use AWS Secrets Manager or App Runner environment variables

3. **Deployment workflow**:
   - Develop features in feature branches
   - Create pull requests for code review
   - Merge to main branch only when ready to deploy
   - Monitor App Runner logs during deployment

## Step 5: Managing Updates and Deployments

### Manual Deployments

1. **Trigger manual deployment**:
   - Go to App Runner console > select your service
   - Click "Deploy" button at the top
   - This rebuilds your application using the latest code

2. **Deployment options**:
   - If using ECR, you can deploy a specific image tag
   - If using GitHub, you can deploy from a specific commit

### Monitor Deployments

1. **View deployment logs**:
   - In App Runner console, select your service
   - Click "Logs" tab
   - View "Build logs" or "Deployment logs"
   - These logs help diagnose build or deployment issues

2. **View application logs**:
   - In the "Logs" tab, select "Application logs"
   - These show runtime logs from your Streamlit application
   - Useful for troubleshooting application errors

### Rollback to Previous Version

1. **Access deployment history**:
   - In App Runner console, select your service
   - Click "Activity" tab
   - View list of past deployments

2. **Perform rollback**:
   - Find the working deployment in the list
   - Click "Deploy" next to that version
   - App Runner will redeploy that specific version

## Step 6: Troubleshooting

### Common Issues and Solutions

1. **Build failures**:
   - **Symptom**: Deployment fails during build phase
   - **Check**: Build logs for package installation errors
   - **Solution**: Update requirements.txt, check Python version compatibility

2. **Application startup failures**:
   - **Symptom**: Service deploys but shows unhealthy status
   - **Check**: Application logs for runtime errors
   - **Solution**: Check start command, port configuration, and environment variables

3. **Custom domain issues**:
   - **Symptom**: Domain verification fails or doesn't resolve
   - **Check**: DNS records in Route 53, certificate status
   - **Solution**: Verify CNAME records match exactly what App Runner provides

4. **Performance problems**:
   - **Symptom**: Application runs slowly or crashes
   - **Check**: Resource utilization metrics
   - **Solution**: Increase CPU/memory allocation or max instances

### Debugging Techniques

1. **Enhanced logging**:
   - Add detailed logging in your Streamlit app
   - Log key events and variable states
   - Use `st.write` or Python's logging module

2. **Testing environment variables**:
   - Add a debugging page that displays non-sensitive environment variables
   - Verify variables are correctly set in App Runner

3. **Local testing**:
   - Test with the same Docker container locally
   - Match environment variables and configuration

### AWS Support Resources

- AWS Documentation: [App Runner Documentation](https://docs.aws.amazon.com/apprunner/)
- AWS Support: [AWS Support Center](https://console.aws.amazon.com/support/)
- Stack Overflow: Search for "AWS App Runner" related questions

## Step 7: Cost Management

### App Runner Pricing Structure (as of 2025)

- **Compute**: Pay for vCPU and memory usage per second
  - Example: 1 vCPU and 2 GB memory costs approximately $0.064/hour when running
  - Automatic scale-to-zero when not in use

- **Provisioned concurrency**: Optional standby capacity
  - Keeps your service warm with no cold starts
  - Additional cost for reserved capacity

### Cost Optimization Tips

1. **Right-size your application**:
   - Start with the smallest instance size that meets your needs
   - Monitor performance and scale up only if necessary
   - Streamlit apps typically work well with 1 vCPU/2 GB memory

2. **Auto-scaling configuration**:
   - Set minimum instances to 1 (or 0 for least cost)
   - Set reasonable maximum instances to prevent unexpected costs
   - Monitor usage patterns and adjust accordingly

3. **Set up budget alerts**:
   - Use AWS Budgets to set up alerts
   - Get notified when costs exceed expected amount
   - Add budget actions to pause services if costs spike

### Estimated Monthly Costs

| Configuration | Estimated Cost (30 days, 24/7) | Notes |
|---------------|--------------------------------|-------|
| 1 vCPU, 2 GB, always on | ~$46 | No auto-scaling to zero |
| 1 vCPU, 2 GB, 8 hours/day | ~$15 | Manual pause/resume |
| 1 vCPU, 2 GB, auto-scaling | ~$5-$20 | Depends on traffic |

*Add approximately $0.50/month for Route 53 hosted zone + domain registration fee ($12-15/year)*

## Step 8: Security Considerations

### Securing Sensitive Information

1. **API keys and secrets**:
   - Use environment variables in App Runner configuration
   - For higher security, use AWS Secrets Manager:
     ```bash
     # Create secret
     aws secretsmanager create-secret --name portfolio/anthropic-api-key --secret-string "your-api-key"
     
     # Reference in App Runner
     # Add environment variable:
     # ANTHROPIC_API_KEY: /aws/reference/secretsmanager/portfolio/anthropic-api-key
     ```

2. **IAM roles and permissions**:
   - Create a dedicated IAM role for your App Runner service
   - Apply principle of least privilege (only necessary permissions)

3. **Network security**:
   - App Runner provides built-in DDoS protection
   - Consider using AWS WAF for additional protection against common web exploits

### Compliance and Best Practices

1. **Regular updates**:
   - Keep dependencies updated for security patches
   - Use dependabot or similar tools to automate updates

2. **Logging and monitoring**:
   - Enable enhanced logging for security events
   - Set up CloudWatch alarms for unusual activity

3. **Regular security review**:
   - Periodically review IAM permissions
   - Scan code for vulnerabilities

## Conclusion

AWS App Runner provides a streamlined, cost-effective solution for deploying your Streamlit portfolio application. By following this guide, you've set up a scalable, secure deployment with CI/CD integration and custom domain support.

The automatic scaling capabilities ensure your site remains responsive under varying traffic conditions while minimizing costs when traffic is low. The built-in GitHub integration simplifies your development workflow, allowing you to focus on enhancing your portfolio rather than managing infrastructure.

## Appendix: Useful Commands Reference

### AWS CLI Commands for App Runner

```bash
# List App Runner services
aws apprunner list-services

# Describe specific service
aws apprunner describe-service --service-arn arn:aws:apprunner:region:account:service/service-name/service-id

# Pause service (to save costs)
aws apprunner pause-service --service-arn arn:aws:apprunner:region:account:service/service-name/service-id

# Resume service
aws apprunner resume-service --service-arn arn:aws:apprunner:region:account:service/service-name/service-id

# Delete service
aws apprunner delete-service --service-arn arn:aws:apprunner:region:account:service/service-name/service-id
```

### Docker Commands for Local Testing

```bash
# Build image
docker build -t portfolio-app .

# Run container
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=your-key portfolio-app

# View logs
docker logs [container-id]

# Interactive shell
docker exec -it [container-id] /bin/bash
```

### GitHub CLI Commands for Repository Management

```bash
# Clone repository
gh repo clone username/portfolio-app

# Create pull request
gh pr create --title "Update feature" --body "Description of changes"

# View workflow runs
gh run list
```
