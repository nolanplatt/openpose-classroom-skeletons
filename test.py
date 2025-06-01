# test.py
# Used to verify that pyopenpose is installed correctly. Try running this script after installing OpenPose (with Python bindings). 
# Can be helpful for debugging Python installation rather than having to test the whole script.

# @author Nolan Platt (nolanplatt.com)
# @date 6/1/2025

import sys
try:
    import pyopenpose as op
    print("pyopenpose working. version:", op.__version__)
except Exception as e:
    print("FAILED to import pyopenpose:\n", e)
    sys.exit(1)

