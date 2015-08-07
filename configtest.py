#main.py
import os
import config

print config.__file__
print os.path.basename(config.__file__)
print os.path.dirname(config.__file__)