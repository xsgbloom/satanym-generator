# Use an official lightweight Python image.
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app

# Create a non-privileged user and group for security.
# This prevents potential container breakout attacks from having root access.
RUN groupadd -r satanym && useradd -r -g satanym satanym

WORKDIR $APP_HOME

# Install production dependencies.
# We copy requirements first to leverage Docker's layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image.
COPY . .

# Change ownership of the application directory to the non-root user.
RUN chown -R satanym:satanym $APP_HOME

# Switch to the non-privileged user.
USER satanym

# Run the web service on container startup.
# 'exec' allows uvicorn to receive SIGTERM signals for graceful termination.
# We use a single worker to optimize for Cloud Run's 'Scale to 0' behavior.
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
