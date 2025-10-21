# Use AWS Lambda Python 3.13 base image
FROM public.ecr.aws/lambda/python:3.13

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project files
COPY mhmas/ ${LAMBDA_TASK_ROOT}/mhmas/
COPY api/ ${LAMBDA_TASK_ROOT}/api/
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}/
COPY manage.py ${LAMBDA_TASK_ROOT}/

# Set environment variable for Django settings
ENV DJANGO_SETTINGS_MODULE=mhmas.settings

# Set the Lambda handler
CMD ["lambda_handler.handler"]