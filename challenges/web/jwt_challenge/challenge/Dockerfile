# Use an official Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install --production

# Copy the rest of the application
COPY . .

# Expose the app port (you can change this if your app uses a different port)
EXPOSE 3000

# Start the Node.js app
CMD ["node", "index.js"]
