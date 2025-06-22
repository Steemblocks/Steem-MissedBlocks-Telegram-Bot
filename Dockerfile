FROM python:3.10-alpine

# Install system dependencies required for building some Python packages
RUN apk add --no-cache gcc musl-dev libffi-dev

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY steem_bot.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "steem_bot.py"]
