#The name of the base image to use.
#Set the base image to use for any subsequent instructions that follow.
#use an official Python runtime as a parent image
FROM  python:3.8-slim

#he absolute or relative path to use as the working directory. Will be created if it does not exist.
#Set the working directory for any ADD, COPY, CMD, ENTRYPOINT, or RUN instructions that follow.
#set the workoing directory in the containner
WORKDIR  /app

#The name of the destination file or folder.
#Copy new files and directories to the image's filesystem.
#Install the current directory contents into the container at /app
COPY . /app

## INstall Falsk in the container
RUN  pip install flask sqlalchemy psycopg2-binary 

#The port that this container should listen on.
#Define network ports for this container to listen on at runtime.
# Make port 5000 available to the world outside 
EXPOSE 5001

# Run app.py when the container launches
CMD ["python", "app.py"]

