FROM python:3.14.3-slim

WORKDIR /app

# Copy files
COPY . .

# Install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create required folders
RUN mkdir -p logs reports plots

# Default command
ENTRYPOINT [ "python", "main.py" ]