# Deployment Guide for Portfolio Website

This guide provides instructions for deploying your portfolio website to various platforms.

## Local Development

### Prerequisites

- Python 3.9+ installed
- pip (Python package manager)

### Setup

1. Clone or download the portfolio application

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (optional for Claude integration)
   ```bash
   cp .env.example .env
   # Edit .env to add your Anthropic API key
   ```

4. Run the application
   ```bash
   streamlit run app.py
   ```
   
   Or for the standalone version:
   ```bash
   streamlit run standalone_portfolio.py
   ```

## Cloud Deployment Options

### Deployment Options Summary

| Platform | Pros | Cons | Best For |
|----------|------|------|----------|
| Streamlit Cloud | Easiest setup, free tier available | Limited customization | Quick deployment, portfolio sharing |
| Heroku | Easy deployment, good free tier | Dyno sleep on free tier | Development, testing |
| AWS Elastic Beanstalk | Highly scalable, full control | More complex setup, costs | Production, high-traffic portfolios |
| Docker | Consistent environment, portable | Requires Docker knowledge | Local development, custom hosting |
| Google Cloud Platform | Highly scalable, custom domain, SSL | Learning curve, potential costs | Production with custom domain |

For Google Cloud Platform deployment with custom domain and SSL, see the [GCP Deployment Guide](GCP_DEPLOYMENT.md).

### Streamlit Cloud (Recommended)

The easiest way to deploy your portfolio site is using [Streamlit Cloud](https://streamlit.io/cloud).

1. Push your code to a GitHub repository

2. Sign up for Streamlit Cloud and connect your GitHub account

3. Deploy your app by pointing to your GitHub repository and the main app file

4. Configure your Anthropic API key as a secret in the Streamlit Cloud dashboard

### Heroku

1. Create a `Procfile` in your project root with:
   ```
   web: streamlit run app.py --server.port=$PORT
   ```

2. Create a `runtime.txt` file with your Python version:
   ```
   python-3.11.0
   ```

3. Deploy to Heroku:
   ```bash
   heroku create your-portfolio-name
   git push heroku main
   ```

4. Set environment variables:
   ```bash
   heroku config:set ANTHROPIC_API_KEY=your_api_key
   ```

### AWS Elastic Beanstalk

1. Install the EB CLI and initialize your application:
   ```bash
   pip install awsebcli
   eb init -p python-3.11 portfolio-app
   ```

2. Create a `.ebextensions/01_streamlit.config` file:
   ```yaml
   option_settings:
     aws:elasticbeanstalk:application:environment:
       ANTHROPIC_API_KEY: your_api_key
     aws:elasticbeanstalk:container:python:
       WSGIPath: app.py
   ```

3. Create a `Procfile`:
   ```
   web: streamlit run app.py --server.port=8080
   ```

4. Deploy:
   ```bash
   eb create portfolio-env
   ```

### Google Cloud Platform Deployment

For detailed instructions on deploying to Google Cloud Platform with a custom domain, see the [GCP Deployment Guide](GCP_DEPLOYMENT.md).

Key benefits of GCP deployment:
- Serverless container deployment with Cloud Run
- Automatic SSL certificate provisioning and renewal
- Custom domain mapping
- Autoscaling based on traffic
- CI/CD integration options
- Pay-per-use pricing model (with generous free tier)

## Docker Deployment

### Local Docker

1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt ./
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "app.py"]
   ```

2. Build and run:
   ```bash
   docker build -t portfolio-app .
   docker run -p 8501:8501 -e ANTHROPIC_API_KEY=your_api_key portfolio-app
   ```

### Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  portfolio:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: kelby-portfolio
    ports:
      - "8501:8501"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
    volumes:
      - .:/app
    restart: unless-stopped
```

Run with:
```bash
docker-compose up
```

### Windows Docker Desktop

For easy deployment on Windows using Docker Desktop:

1. Download and extract the portfolio_project.tar.gz file using a tool like 7-Zip

2. Open Command Prompt or PowerShell and navigate to the extracted portfolio_app directory:
   ```
   cd path\to\portfolio_app
   ```

3. Run the provided deploy.bat script by double-clicking it or executing it from Command Prompt:
   ```
   deploy.bat
   ```
   
4. The script will:
   - Check if Docker Desktop is running
   - Prompt for an optional Anthropic API key
   - Build and start the Docker container

5. Once deployed, access your portfolio at:
   ```
   http://localhost:8501
   ```

6. To stop the application, run:
   ```
   docker-compose down
   ```

Note: Ensure Docker Desktop is installed and running before attempting deployment. The application can be restarted at any time by running `docker-compose up -d` in the portfolio_app directory.

## Customization

### Changing Personal Information

Edit the `data/resume_data.py` file to update your personal information, work experience, skills, and other resume details.

### Styling

Modify the `styles/main.css` file to change the visual appearance of your portfolio.

### Adding More Sections

To add new sections to your portfolio:

1. Create a new component in the `components/` directory
2. Import and add the component to the main `app.py` file

## Security Notes

- Never commit your API keys to version control
- Use environment variables or secrets management for sensitive information
- Consider setting up a proxy API for Claude to avoid exposing your API key in the frontend

## Troubleshooting

### Common Issues

- **Port already in use**: Change the port using `--server.port` when running Streamlit
- **API key errors**: Double-check that your Anthropic API key is correct and properly set
- **Missing dependencies**: Ensure all requirements are installed with `pip install -r requirements.txt`
- **Import errors**: Check the import paths in your components

### Getting Help

If you encounter issues:

- Check the [Streamlit documentation](https://docs.streamlit.io/)
- Ask for help on the [Streamlit Community Forum](https://discuss.streamlit.io/)
- For Claude API issues, refer to the [Anthropic documentation](https://docs.anthropic.com/)

## Continuous Integration / Continuous Deployment (CI/CD)

For production deployments, consider setting up CI/CD pipelines:

- **GitHub Actions**: Workflows for automatic deployment to Streamlit Cloud, Heroku, AWS, or GCP
- **GitLab CI/CD**: Similar to GitHub Actions
- **Jenkins**: For more complex build and deployment processes

Example GitHub Actions workflows are included in the following guides:
- AWS Elastic Beanstalk deployment section
- GCP Cloud Run deployment guide

## Domain Management

When using your own domain:

1. Register a domain with a registrar (e.g., Namecheap, Google Domains, GoDaddy)
2. Configure DNS settings as specified in the platform-specific instructions:
   - Streamlit Cloud: Add CNAME records
   - Heroku: Add DNS target records
   - AWS: Use Route 53 or add CNAME records
   - GCP: Add records as specified in the GCP guide

## SSL Certificates

For secure HTTPS connections:

- Streamlit Cloud: Automatically provisioned
- Heroku: Automatically provisioned
- AWS: Use AWS Certificate Manager
- GCP: Automatically provisioned for mapped domains
- Custom setups: Consider Let's Encrypt for free certificates