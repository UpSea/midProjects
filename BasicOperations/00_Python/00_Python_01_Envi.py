import math

# 1) Showing all functions in an imported module
for n in dir(math):
    print(n)
    
# 2) Deleting an imported module
print(dir())
del math
print(dir())

# 3) Finding the location of an imported module
import numpy as np
print(np.__file__)
print(np)

import sys

print(sys.path())