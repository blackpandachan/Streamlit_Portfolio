# Google Cloud Platform Deployment Guide

This guide provides step-by-step instructions for deploying your portfolio application to Google Cloud Platform with your custom domain.

## Prerequisites

- A Google Cloud Platform account
- Google Cloud SDK installed locally
- Docker installed locally
- An existing domain name registered and managed by you
- Basic familiarity with GCP services and command line

## Deployment Options

There are multiple ways to deploy your Streamlit portfolio app on GCP. The two recommended approaches are:

1. **Cloud Run** (Recommended): Serverless, pay-per-use, autoscaling container service
2. **Google Kubernetes Engine (GKE)**: For more complex deployments with high availability needs

This guide will focus primarily on Cloud Run as it's the most cost-effective and straightforward option.

## Option 1: Google Cloud Run Deployment

### Step 1: Set Up Google Cloud Environment

1. Create a new GCP project (or select an existing one):
   ```bash
   gcloud projects create kelby-portfolio --name="Kelby Portfolio"
   gcloud config set project kelby-portfolio
   ```

2. Enable required APIs:
   ```bash
   gcloud services enable artifactregistry.googleapis.com run.googleapis.com
   ```

3. Create a Docker repository in Artifact Registry:
   ```bash
   gcloud artifacts repositories create portfolio-repo \
     --repository-format=docker \
     --location=us-west1 \
     --description="Portfolio app repository"
   ```

### Step 2: Build and Push the Docker Image

1. Authenticate Docker to Artifact Registry:
   ```bash
   gcloud auth configure-docker us-west1-docker.pkg.dev
   ```

2. Build and tag your Docker image:
   ```bash
   docker build -t us-west1-docker.pkg.dev/kelby-portfolio/portfolio-repo/portfolio-app:latest .
   ```

3. Push the image to Artifact Registry:
   ```bash
   docker push us-west1-docker.pkg.dev/kelby-portfolio/portfolio-repo/portfolio-app:latest
   ```

### Step 3: Deploy to Cloud Run

1. Deploy your container to Cloud Run:
   ```bash
   gcloud run deploy portfolio-app \
     --image=us-west1-docker.pkg.dev/kelby-portfolio/portfolio-repo/portfolio-app:latest \
     --platform=managed \
     --region=us-west1 \
     --allow-unauthenticated \
     --port=8501 \
     --set-env-vars="ANTHROPIC_API_KEY=your_api_key"
   ```

2. Once deployed, you'll receive a service URL that looks like:
   ```
   https://portfolio-app-abc123-uc.a.run.app
   ```

### Step 4: Configure Your Custom Domain

1. Map your custom domain to your Cloud Run service:

   First, add the domain to your project:
   ```bash
   gcloud domains verify example.com
   ```

   Then, map it to your Cloud Run service:
   ```bash
   gcloud beta run domain-mappings create \
     --service=portfolio-app \
     --domain=www.example.com \
     --region=us-west1
   ```

2. The command will output the DNS records you need to configure with your domain registrar:
   ```
   NAME                 TYPE   DATA
   www.example.com.     CNAME  ghs.googlehosted.com.
   ```

3. Go to your domain registrar's DNS settings and add these records.

4. Wait for DNS propagation (can take 24-48 hours) before your custom domain works.

### Step 5: Set Up SSL Certificate

Cloud Run automatically provisions and renews SSL certificates for mapped domains.

### Step 6: Configure Service Settings (Optional)

Fine-tune your Cloud Run service:

1. Set up autoscaling:
   ```bash
   gcloud run services update portfolio-app \
     --min-instances=0 \
     --max-instances=10 \
     --region=us-west1
   ```

2. Configure memory limits:
   ```bash
   gcloud run services update portfolio-app \
     --memory=1Gi \
     --region=us-west1
   ```

## Option 2: Google Kubernetes Engine (GKE) Deployment

For more complex scenarios, you can deploy to GKE:

### Step The1: Create a GKE Cluster

```bash
gcloud container clusters create portfolio-cluster \
  --zone us-west1-a \
  --num-nodes=1 \
  --machine-type=e2-small
```

### Step 2: Create Kubernetes Deployment Files

Create `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: portfolio-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: portfolio-app
  template:
    metadata:
      labels:
        app: portfolio-app
    spec:
      containers:
      - name: portfolio-app
        image: us-west1-docker.pkg.dev/kelby-portfolio/portfolio-repo/portfolio-app:latest
        ports:
        - containerPort: 8501
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: portfolio-secrets
              key: anthropic-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

Create `service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: portfolio-service
spec:
  selector:
    app: portfolio-app
  ports:
  - port: 80
    targetPort: 8501
  type: ClusterIP
```

### Step 3: Create Kubernetes Secret for API Key

```bash
kubectl create secret generic portfolio-secrets --from-literal=anthropic-api-key=your_api_key
```

### Step 4: Apply Kubernetes Configurations

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### Step 5: Set Up Ingress and Domain

1. Enable Ingress:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.7.0/deploy/static/provider/cloud/deploy.yaml
   ```

2. Create ingress.yaml:
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: portfolio-ingress
     annotations:
       kubernetes.io/ingress.class: "nginx"
       cert-manager.io/cluster-issuer: "letsencrypt-prod"
   spec:
     tls:
     - hosts:
       - portfolio.example.com
       secretName: portfolio-tls
     rules:
     - host: portfolio.example.com
       http:
         paths:
         - path: /
           pathType: Prefix
           backend:
             service:
               name: portfolio-service
               port:
                 number: 80
   ```

3. Apply the ingress configuration:
   ```bash
   kubectl apply -f ingress.yaml
   ```

4. Configure DNS with your domain registrar.

## Continuous Deployment (CI/CD)

To automate deployments:

### GitHub Actions for Cloud Run

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v1
      with:
        project_id: kelby-portfolio
        service_account_key: ${{ secrets.GCP_SA_KEY }}
        
    - name: Configure Docker
      run: gcloud auth configure-docker us-west1-docker.pkg.dev
      
    - name: Build and push Docker image
      run: |
        docker build -t us-west1-docker.pkg.dev/kelby-portfolio/portfolio-repo/portfolio-app:${{ github.sha }} .
        docker push us-west1-docker.pkg.dev/kelby-portfolio/portfolio-repo/portfolio-app:${{ github.sha }}
        
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy portfolio-app \
          --image=us-west1-docker.pkg.dev/kelby-portfolio/portfolio-repo/portfolio-app:${{ github.sha }} \
          --platform=managed \
          --region=us-west1 \
          --allow-unauthenticated
```

## Monitoring and Management

1. Set up monitoring in Google Cloud Console:
   - Go to Cloud Run service
   - Navigate to the "Metrics" tab

2. Set up Cloud Logging:
   ```bash
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=portfolio-app" --limit 10
   ```

## Cost Optimization

Google Cloud Run is very cost-effective:
- You only pay when your service is processing requests
- Free tier includes 2 million requests/month, 360,000 GB-seconds of memory, and 180,000 vCPU-seconds
- Set min-instances=0 to allow the service to scale to zero when not in use

## Troubleshooting

1. **Deployment Failures**:
   ```bash
   gcloud run revisions list --service=portfolio-app --region=us-west1
   ```

2. **Container Issues**:
   ```bash
   gcloud run services logs read portfolio-app --region=us-west1
   ```

3. **Domain Mapping Issues**:
   - Verify DNS settings with `dig www.example.com`
   - Check domain mapping status: `gcloud beta run domain-mappings describe --domain=www.example.com --region=us-west1`

4. **Common Issues**:
   - Ensure the Docker container is exposing port 8501
   - Make sure Streamlit is configured to accept external connections (`--server.address=0.0.0.0`)
   - Check resource limits if the container is crashing

## Security Best Practices

1. Store API keys in Secret Manager:
   ```bash
   gcloud secrets create anthropic-api-key --data-file=api-key.txt
   ```

2. Reference secrets in Cloud Run:
   ```bash
   gcloud run services update portfolio-app \
     --set-secrets=ANTHROPIC_API_KEY=anthropic-api-key:latest \
     --region=us-west1
   ```

3. Set up Identity and Access Management (IAM):
   ```bash
   gcloud projects add-iam-policy-binding kelby-portfolio \
     --member=serviceAccount:portfolio-service@kelby-portfolio.iam.gserviceaccount.com \
     --role=roles/secretmanager.secretAccessor
   ```
