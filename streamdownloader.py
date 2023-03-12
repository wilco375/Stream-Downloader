import os
import time
import subprocess

# Get pid of this process
pidfile = os.path.join(os.path.dirname(__file__), 'pid')
if os.path.exists(pidfile):
    with open(pidfile) as f:
        pid = int(f.read())

    # If already running, and pid is streamdownloader.py, exit
    try:
        if os.path.basename(__file__) in subprocess.check_output(['ps', '-o', 'cmd=', str(pid)]).decode('utf-8'):
            print('Process already running, exiting...')
            exit()
    except subprocess.CalledProcessError:
        pass

# Write pid to file
with open(pidfile, 'w') as f:
    f.write(str(os.getpid()))

streams = {}
while True:
    # Get new list of streams
    streams_file = os.path.join(os.path.dirname(__file__), 'config', 'streams.txt')
    if not os.path.exists(streams_file):
        # Create empty file
        os.makedirs(os.path.dirname(streams_file), exist_ok=True)
        with open(streams_file, 'w') as f:
            pass
    with open(streams_file) as f:
        new_streams = [stream.strip() for stream in f.read().splitlines() if stream.strip() != '' and not stream.startswith('#')]
    
    for new_stream in new_streams:
        if new_stream not in streams:
            streams[new_stream] = {
                'process': None
            }

    for stream in streams.keys():
        if stream not in new_streams:
            streams[stream]['process'].kill()
            del streams[stream]
        else:
            if streams[stream]['process'] is None or streams[stream]['process'].poll() is not None:
                # Filename is stream name (all alphanumeric characters after last slash of url (with slashes stripped) and time)
                filename = ''.join([c for c in stream.strip('/').split('/')[-1] if c.isalnum()]) + '-' + time.strftime('%Y%m%d%H%M%S') + '.mp4'
                filename = os.path.join(os.path.dirname(__file__), 'output', filename)
                os.makedirs(os.path.dirname(filename), exist_ok=True)

                # streamlink --twitch-disable-ads --stdout <stream> best | ffmpeg -i - -c copy <filename>
                streams[stream]['process'] = subprocess.Popen(['streamlink', '--twitch-disable-ads', '--stdout', stream, '1080p,1080p50,1080p60,best'], stdout=subprocess.PIPE)
                streams[stream]['process'] = subprocess.Popen(['ffmpeg', '-i', '-', '-c', 'copy', filename], stdin=streams[stream]['process'].stdout)

    # Check for new streams every minute
    time.sleep(60)
