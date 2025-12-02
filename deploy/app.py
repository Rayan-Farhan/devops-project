import json
import os
import joblib
import numpy as np
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Global variable to hold the loaded model (Cold Start optimization)
model = None
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

def load_model():
    """
    Load the model from disk.
    """
    global model
    if model is None:
        try:
            if os.path.exists(MODEL_PATH):
                logger.info(f"Loading model from {MODEL_PATH}")
                model = joblib.load(MODEL_PATH)
                logger.info("Model loaded successfully.")
            else:
                logger.error(f"Model file not found at {MODEL_PATH}")
                raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise e

def lambda_handler(event, context):
    """
    AWS Lambda Handler function.
    """
    # Load model if not already loaded
    load_model()

    try:
        # Parse input body
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event

        logger.info(f"Received event: {json.dumps(body)}")

        # Validate input
        if 'features' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing "features" key in input data.'})
            }
        
        features = body['features']
        
        if not isinstance(features, list) or len(features) == 0:
             return {
                'statusCode': 400,
                'body': json.dumps({'error': '"features" must be a non-empty list.'})
            }

        # Prepare data for prediction
        # Reshape to 2D array as expected by scikit-learn (1 sample, n features)
        input_data = np.array(features).reshape(1, -1)

        # Make prediction
        prediction = model.predict(input_data)[0]
        
        # Get probability if the model supports it
        probability = None
        if hasattr(model, 'predict_proba'):
            try:
                # Assuming binary classification, getting prob of class 1
                probs = model.predict_proba(input_data)
                probability = probs[0].tolist() # Convert to list for JSON serialization
            except Exception as e:
                logger.warning(f"Could not retrieve probabilities: {e}")

        # Construct response
        response_body = {
            'prediction': int(prediction), # Convert numpy int to python int
            'probability': probability
        }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(response_body)
        }

    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)})
        }
