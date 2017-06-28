# Copyright 2014-2017, The University of Edinburgh.
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
count_frequency tests

These tests expect:
- count_frequency to be in the path or the current directory.
- Input files to be in a samples/ directory:
  - events2013.dat
- Test oracle files to be in a testoracle/ directory:
  - freqs_events2013.dat created via
    count_frequency samples/events2013.dat testoracle/freqs_events2013.dat
  - freqs5_events2013.dat created via
    count_frequency samples/events2013.dat testoracle/freqs5_events2013.dat 5
"""

import numpy as np
import os
import os.path
import subprocess


def compare_files(file_name1, file_name2):
    """
    Compare two files, line by line, for equality.
    Arguments:
        file_name1 (str or unicode): file name.
        file_name2 (str or unicode): file name.
    Returns:
        bool: True if files are equal, False otherwise.
    """
    with open(file_name1) as file1, open(file_name2) as file2:
        for line1, line2 in zip(file1, file2):
            if line1 != line2:
                file1.close()
                file2.close()
                return False
    file1.close()
    file2.close()
    return True


def delete_files(directory, suffix):
    """
    Delete all files ending in a suffix from a specific directory.
    """
    for file_name in os.listdir(directory):
        if file_name.endswith(suffix):
            path = os.path.join(directory, file_name)
            try:
                if os.path.isfile(path):
                    os.remove(path)
            except OSError as error:
                # Don't care, but warn user.
                print(error)


def test_count_frequency():
    """
    Test count_frequency.
    """
    cmd = "count_frequency samples/events2013.dat freqs_events2013.dat"
    result = subprocess.call(cmd, shell=True)
    assert 0 == result, "Unexpected return code"
    assert os.path.isfile("freqs_events2013.dat"),\
        "Could not find freqs_events2013.dat"
    actual = np.loadtxt("freqs_events2013.dat")
    expected = np.loadtxt("testoracle/freqs_events2013.dat")
    np.testing.assert_almost_equal(expected,
                                   actual,
                                   2,
                                   "freqs_events2013.dat does not match file on testoracle")


def test_minimum_token_length():
    """
    Test count_frequency with a minimum token length.
    """
    cmd = "count_frequency samples/events2013.dat freqs5_events2013.dat 5"
    result = subprocess.call(cmd, shell=True)
    assert 0 == result, "Unexpected return code"
    assert os.path.isfile("freqs5_events2013.dat"),\
        "Could not find freqs5_events2013.dat"
    actual = np.loadtxt("freqs5_events2013.dat")
    expected = np.loadtxt("testoracle/freqs5_events2013.dat")
    np.testing.assert_almost_equal(expected,
                                   actual,
                                   2,
                                   "freqs5_events2013.dat does not match file on testoracle")


def test_missing_output_file_name():
    """
    Test count_frequency with a missing output file name.
    """
    cmd = "count_frequency samples/events2013.dat"
    result = subprocess.call(cmd, shell=True)
    assert 0 != result, "Unexpected return code"
