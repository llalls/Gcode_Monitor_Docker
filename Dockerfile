# Use an official Python runtime as a parent image
FROM python:3.7.9

# Set the working directory to /app
WORKDIR /app

# copy requirements.txt file to load initial enviroment packages
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy everything in gcode-object-monitor to the current folder, which means to /app
# because we set /app as our WORKDIR of Docker
COPY ./gcode-object-monitor /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]