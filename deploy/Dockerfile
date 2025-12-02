FROM amazon/aws-lambda-python:3.10

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy function code and model
COPY app.py .
# Note: model.pkl must be present in the build context (deploy/ folder)
COPY model.pkl .
COPY utils/ ./utils/

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD ["app.lambda_handler"]
