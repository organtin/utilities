import re
import os
import subprocess
from subprocess import PIPE
import sys
from itertools import combinations
import filecmp
'''
    findDuplicates.py - find duplicated files in your disk
    Copyright (C) 2023 giovanni.organtini@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

# this must be improved: takes the first argument as the directory to navigate
f = sys.argv[1]

print(f'findDuplicates.py - Copyright (C) 2023 giovanni.organtini@gmail.com')
print(f'This program comes with ABSOLUTELY NO WARRANTY; for details')
print(f'see <https://www.gnu.org/licenses/>.')
print(f'This is free software, and you are welcome to redistribute it')
print(f'under certain conditions, as detailed in the license.')
print(f'\nType anything to continue')

x = input()
print(f'\nFinding duplicates in {f}. Please be patient...')

# find files
cmd = 'find ' + f + ' -path \*.DS_Store -prune -o -type f -exec md5 {} \;'
output = subprocess.run(cmd, stdout = PIPE, stderr = PIPE, shell = True)
files = output.stdout.decode("utf-8").split('\n')

# remove the last, empty, string
files = files[:-1]

# check if there are duplicates
fullFilenames = [re.sub('MD5 \((.*)\) =.*','\\1', f) for f in files]
filenames = []
filenames = [os.path.basename(f) for f in fullFilenames]
md5 = {}
for f in files:
    key = re.sub('.*\) = ', '', f)
    if key not in md5:
        md5[key] = []
    md5[key].append(re.sub('MD5 \((.*)\) =.*','\\1', f))

# md5 is a dictionary that associates the md5 key of each file to its name
md5keys = list(set(list(md5.keys())))

for k in md5keys:
    if len(md5[k]) > 1:
        # if there are multiple files with the same key, they are the same file
        print('Found multiple copies of the following files:')
        i = 0
        # show the list of identical files
        for c in md5[k]:
            print(f'{i:5d}: {c}')
            i += 1
        # ask the user what to do
        x = input('Remove (q to exit): ')
        if 'q' in x or 'Q' in x:
            print('Exiting...')
            exit(0)
        # try to remove the indicated files
        try:
            xl = x.split(',')
            for x in xl:
                j = int(x)
                if j >= 0:
                    print(f'rm -f {md5[k][j]}')
                    os.remove(md5[k][j])
        except:
            print('cannot get your answer')


