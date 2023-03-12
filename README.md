# Stream downloader
Simple docker image that monitors live stream channels and downloads them to an mp4 file if they are online using [streamlink](https://streamlink.github.io/).

## Build and run
Build and run using docker:  
```bash
docker build -t streamdownloader .
docker run --restart=always -d -v /path/to/config:/app/config -v /path/to/output:/app/output streamdownloader
```

Or use docker-compose instead:
```yaml
version: '3'

services:
  streamdownloader:
    image: streamdownloader
    restart: always
    volumes:
      - /path/to/config:/app/config
      - /path/to/output:/app/output
```

## Configure
To monitor a channel, add the channel urls to `config/streams.txt`, separated by newlines, e.g.
```
https://www.twitch.tv/<channel1>
https://www.twitch.tv/<channel2>
https://www.youtube.com/@<channel3>
```
All urls supported by streamlink are supported.