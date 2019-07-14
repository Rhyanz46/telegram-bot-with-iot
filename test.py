import os
import sys

pathname = os.path.dirname(sys.argv[0])
root_lokasi = os.path.abspath(pathname)
ddd = os.path.abspath(os.path.join(pathname, 'foto'))


print(ddd)

