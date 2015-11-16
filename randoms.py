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

"""
Create a file of random numbers.

Usage: python randoms.py FILE MAX_RANDOM MAX_VALUES [SEED]

Creates a file, FILE, consisting of MAX_VALUES integers, one per line
each value being randomly chosen between 0 and MAX_RANDOM. If SEED
is given then the random seed is set to this.
"""

import random
import sys


def main(arguments):
    """
    Create a file of random numbers. The file consists of a number of
    random values, ranging from 0 to a maximum random value. If a seed
    is provided then this is used to seed the random numbers.

    Arguments:
        arguments (list[str or unicode]): file name, maximum random
            value, number of random values and (optional) seed.
    """
    file_name = arguments[1]
    max_random = int(arguments[2])
    max_values = int(arguments[3])
    if len(arguments) == 5:
        random.seed(int(arguments[4]))
    random_file = open(file_name, 'w')
    for _ in range(0, max_values):
        random_file.write("%s\n" % str(random.randint(0, max_random)))
    random_file.close()

if __name__ == '__main__':
    main(sys.argv)
