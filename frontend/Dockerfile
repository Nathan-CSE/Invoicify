# Use the official Node.js image
FROM node:14

# Create and change to the app directory
WORKDIR /app

# Install app dependencies
COPY package.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the frontend port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
