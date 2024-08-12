# Use the official Node.js image
FROM node:latest

# Install necessary packages and Infisical CLI
RUN apt-get update && apt-get install -y curl && \
    curl -1sLf 'https://dl.cloudsmith.io/public/infisical/infisical-cli/setup.deb.sh' | bash && \
    apt-get install -y infisical

# Create and change to the app directory
WORKDIR /app

# Copy application dependency manifests to the container image
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the local code to the container image
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Set up Infisical login and run the application
CMD infisical login -i && infisical run -- node src/app.js