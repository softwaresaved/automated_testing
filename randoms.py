# Copyright 2014-2015, The University of Edinburgh.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

import random
import sys

"""
Create a file of random numbers.

Usage: python randoms.py FILE MAX_RANDOM MAX_VALUES [SEED]

Creates a file, FILE, consisting of MAX_VALUES integers, one per line
each value being randomly chosen between 0 and MAX_RANDOM. If SEED
is given then the random seed is set to this. 
"""

file = sys.argv[1]
max_random = int(sys.argv[2])
max_values = int(sys.argv[3])
if len(sys.argv) == 5:
    random.seed(int(sys.argv[4]))

f = open(file, 'w')
for i in range(0, max_values):
    f.write("%s\n" % str(random.randint(0, max_random)))
f.close()
