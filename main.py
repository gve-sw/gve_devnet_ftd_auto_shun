""" Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied."""

import time
from collections import defaultdict
from datetime import datetime, timedelta
import re
import heapq

# linux based files to observe
from watchdog.observers import Observer

# windows based files to observe 
#from watchdog.observers.polling import PollingObserver as Observer

from watchdog.events import FileSystemEventHandler
from ftd_connector import ftd_connection
import config

# Priority queue for unshunning
unshun_queue = []

def shun_ip(ip):
    for device in config.list_of_ftds:
        try:
            ftd = ftd_connection(**device)
            command = f'shun {ip}'
            response = ftd.send_command_clish(command)
            print(response)
        finally:
            ftd.disconnect()
    unshun_time = datetime.now() + timedelta(days=config.delay)
    heapq.heappush(unshun_queue, (unshun_time, ip))

def unshun_ip(ip):
    for device in config.list_of_ftds:
        try:
            ftd = ftd_connection(**device)
            command = f'no shun {ip}'
            response = ftd.send_command_clish(command)
            print(response)
            print("unshun command for: " + ip)
        finally:
            ftd.disconnect()

class LogFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.ip_counts = defaultdict(int)
        self.last_read_position = 0

    def on_modified(self, event):
        with open(event.src_path, 'r') as f:
            # Move to the last read position
            f.seek(self.last_read_position)
            logs = f.readlines()
            # Update the last read position
            self.last_read_position = f.tell()

        # Extract IP addresses and update counts
        for log in logs:
            match = re.search(r'Calling-Station-ID=(\d+\.\d+\.\d+\.\d+)', log)
            if match:
                ip = match.group(1)
                self.ip_counts[ip] += 1
                if self.ip_counts[ip] >= config.threshold: #change to config file
                    shun_ip(ip)
                    # Reset the counter for this IP
                    self.ip_counts[ip] = 0

# Start watching the log file
observer = Observer()
event_handler = LogFileHandler()
observer.schedule(event_handler, path=config.log_path)
observer.start()

try:
    while True:
        # Unshun IP addresses whose time has come
        while unshun_queue and unshun_queue[0][0] <= datetime.now():
            _, ip = heapq.heappop(unshun_queue)
            unshun_ip(ip)

        time.sleep(1)  # Check every second
finally:
    observer.stop()
    observer.join()