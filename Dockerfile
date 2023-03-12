# From python base image
FROM python:3.10-alpine

# Set working directory
WORKDIR /app

# Install ffmpeg
RUN apk add ffmpeg

# Install streamlink
RUN pip install -U streamlink

# Copy script
COPY streamdownloader.py /app/

# Create /app/config and /app/output
RUN mkdir /app/config && mkdir /app/output

# Define mountpoints
VOLUME /app/config
VOLUME /app/output

# Define entrypoint
ENTRYPOINT ["python", "streamdownloader.py"]

# Run command `docker build -t streamdownloader .` to build the image
# Then run `docker run -it --rm -v /path/to/config:/app/config -v /path/to/output:/app/output streamdownloader` to run the container