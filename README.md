# gve_devnet_ftd_auto_shun
monitors a log file for specific IP address patterns and upon detecting repeated occurrences of an IP address, it triggers a "shun" command on certain network devices. Blocked IPs are queued to be automatically unblocked after a set duration


## Contacts
* Jorge Banegas & Rey Diaz

## Solution Components
* FTD
* ISE
* Python
* Paramiko
* Watchdog

## ISE - Send Radius login fail messages

This project reads a log file that is generated from the ISE console, feel free to follow these steps to replicate the logging used for this project

![/IMAGES/0image.png](/IMAGES/log_step1.png)
![/IMAGES/0image.png](/IMAGES/log_step2.png)
![/IMAGES/0image.png](/IMAGES/log_step3.png)


## Installation/Configuration

Edit the config.py file to include details for the script

```python
list_of_ftds = [
    {
    'device_type': 'cisco_ios',
    'ip': 'x.x.x.x',
    'username': 'username',
    'password': 'password',
    }
]

log_path = '/var/log/remotelogs/ise-auth.log'

# unit of occurences till shun comman will be set
threshold = 2

# unit of time in days till unshun command will be sent
delay = 2
```

## Usage
Install python package depedencies:
    
    $ pip install -r requirements.txt

To launch script:
    
    $ python main.py



# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.