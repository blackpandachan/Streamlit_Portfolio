FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy portfolio application
COPY . .

# Expose Streamlit port
EXPOSE 8509

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8509", "--server.address=0.0.0.0"]