import os
import sys
import json
import logging
import awsgi2
from django.core.wsgi import get_wsgi_application

# Set up logging - CRITICAL for debugging!
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Log Python version on cold start
logger.info(f"=== COLD START ===")
logger.info(f"Python version: {sys.version}")
logger.info(f"Python version info: {sys.version_info}")

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mhmas.settings')

# Initialize Django WSGI application
try:
    logger.info("Initializing Django WSGI application...")
    application = get_wsgi_application()
    logger.info("Django initialized successfully!")
except Exception as e:
    logger.error(f"Failed to initialize Django: {str(e)}", exc_info=True)
    raise

def handler(event, context):
    """
    Lambda entry point with full logging
    """
    logger.info("=== HANDLER INVOKED ===")
    logger.info(f"Request ID: {context.aws_request_id}")
    logger.info(f"Event keys: {list(event.keys())}")
    logger.info(f"Path: {event.get('rawPath', event.get('path', 'unknown'))}")
    logger.info(f"Method: {event.get('requestContext', {}).get('http', {}).get('method', 'unknown')}")
    
    try:
        logger.info("Calling awsgi2.response()...")
        response = awsgi2.response(application, event, context)
        
        logger.info(f"Response status: {response.get('statusCode')}")
        logger.info(f"Response headers: {list(response.get('headers', {}).keys())}")
        
        return response
        
    except Exception as e:
        logger.error(f"ERROR in handler: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e),
                'request_id': context.aws_request_id
            })
        }