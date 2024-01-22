# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code into the container
COPY . /app/

# Expose port 5000, which Flask is running on
EXPOSE 5000

# Define environment variable for Flask to run in production mode
# ENV FLASK_ENV=production
ENTRYPOINT [ "python" ]

CMD [ "./srcs/main.py" ]
# # Command to run your application
# CMD ["python", "srcs/app.py"]