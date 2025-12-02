import requests
import json
import sys

# Configuration
# Replace with your actual API Gateway URL after deployment
API_URL = "https://<API_ID>.execute-api.<AWS_REGION>.amazonaws.com/Prod/predict"

# Sample data (matches the shape expected by the model)
# Example: [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
sample_features = [6, 148, 72, 35, 0, 33.6, 0.627, 50]

def invoke_api(url, features):
    payload = {
        "features": features
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    try:
        print(f"Sending request to {url}...")
        print(f"Payload: {json.dumps(payload)}")
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        try:
            print(json.dumps(response.json(), indent=2))
        except json.JSONDecodeError:
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Error invoking API: {e}")

if __name__ == "__main__":
    # Allow overriding URL via command line argument
    if len(sys.argv) > 1:
        API_URL = sys.argv[1]
        
    if "<API_ID>" in API_URL:
        print("Warning: API_URL contains placeholders. Please update the script or pass the URL as an argument.")
        print("Usage: python invoke_api.py [API_URL]")
    
    invoke_api(API_URL, sample_features)
