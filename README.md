# Diabetes Prediction Serverless API

This project deploys a pre-trained Scikit-learn model (`model.pkl`) as a serverless API using AWS Lambda and Docker. It includes a CI/CD pipeline using GitHub Actions.

## Directory Structure

```
diabetes-prediction-lambda/
│
├── deploy/                 # Docker build context
│   ├── Dockerfile          # Docker definition for Lambda
│   ├── app.py              # Lambda handler code
│   ├── model.pkl           # YOUR MODEL FILE (Place this here)
│   ├── requirements.txt    # Python dependencies
│   └── utils/              # Utility modules
│
├── infrastructure/         # IaC
│   └── template.yaml       # AWS SAM template
│
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions CI/CD
│
├── scripts/                # Helper scripts
│   ├── invoke_api.py       # Python script to call the API
│   └── test_local.sh       # Bash script to build and test locally
│
└── README.md
```

## Prerequisites

1.  **Model File**: You **MUST** place your trained `model.pkl` file into the `deploy/` directory.
2.  **AWS Account**: You need an AWS account with permissions to manage Lambda, ECR, and API Gateway.
3.  **Docker**: Installed locally for testing.
4.  **AWS CLI & SAM CLI**: Optional but recommended for manual deployment.

## Setup Instructions

### 1. Place your Model
Copy your trained pickle file to the deploy folder:
```bash
cp /path/to/your/model.pkl ./deploy/model.pkl
```

### 2. Local Testing
You can build and run the Docker container locally to verify the Lambda handler works.

**Using the helper script (Linux/Mac/WSL):**
```bash
chmod +x scripts/test_local.sh
./scripts/test_local.sh
```

**Manually:**
```bash
# Build
docker build -t diabetes-lambda ./deploy

# Run
docker run -p 9000:8080 diabetes-lambda

# Test (in another terminal)
curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" \
    -d '{"features": [1, 85, 66, 29, 0, 26.6, 0.351, 31]}'
```

## Deployment

### Option A: GitHub Actions (CI/CD)
The project includes a GitHub Actions workflow `.github/workflows/deploy.yml` that automatically builds and deploys the Lambda function on push to `main`.

**Configuration Required:**
1.  Create an **ECR Repository** in AWS (e.g., `diabetes-prediction-repo`).
2.  Create a **Lambda Function** in AWS (e.g., `diabetes-prediction-function`) initially (or let SAM create it first).
3.  Set the following **GitHub Secrets**:
    *   `AWS_ACCESS_KEY_ID`
    *   `AWS_SECRET_ACCESS_KEY`
4.  Update the `env` variables in `.github/workflows/deploy.yml`:
    *   `AWS_REGION`
    *   `ECR_REPOSITORY`
    *   `LAMBDA_FUNCTION_NAME`

### Option B: AWS SAM (Manual)
You can also deploy using AWS SAM.

```bash
sam build -t infrastructure/template.yaml
sam deploy --guided
```

## API Usage

Once deployed, you will get an API Gateway URL (e.g., `https://xyz.execute-api.us-east-1.amazonaws.com/Prod/predict`).

**Request:**
*   **Method**: POST
*   **Body**: JSON
    ```json
    {
        "features": [1, 85, 66, 29, 0, 26.6, 0.351, 31]
    }
    ```

**Response:**
```json
{
    "prediction": 0,
    "probability": [0.9, 0.1]
}
```

**Using the Python Script:**
Update the `API_URL` in `scripts/invoke_api.py` and run:
```bash
python scripts/invoke_api.py
```
