#!/usr/bin/env python3

import os

#pull
os.system('git pull')

#kill running process
os.system("kill $(ps -f | grep -m 1 rumblebot.py | awk '{ printf $2 }')")

#build new image
os.system('python3 /projects/rumblebot/rumblebot.py &')
