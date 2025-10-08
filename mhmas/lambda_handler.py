import os
import awsgi
from django.core.wsgi import get_wsgi_application

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

# Initialize Django WSGI application
application = get_wsgi_application()

def handler(event, context):
    """
    Lambda entry point
    Converts Lambda event to WSGI format and back
    """
    return awsgi.response(application, event, context)