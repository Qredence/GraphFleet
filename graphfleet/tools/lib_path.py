## This script is used to get the path to the graphrag library.


import sys
import os


# Add the graphfleet directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graphfleet.libs import graphrag
print(os.path.dirname(graphrag.__file__))