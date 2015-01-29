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
count_frequency tests

These tests expect:
- count_frequency to be in the path or the current directory.
- Input files to be in a samples/ directory:
  - events2013.dat
- Test oracle files to be in a testoracle/ directory:
  - freqs2013.dat created via 
    count_frequency samples/events2013.dat testoracle/freqs2013.dat
  - freqs2013_5.dat created via 
    count_frequency samples/events2013.dat testoracle/freqs2013.dat 5
"""

import numpy as np
import os
import os.path
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_true

"""
Compare two files, line by line, for equality.
"""
def compare_files(file1, file2):
  with open(file1) as f1, open(file2) as f2:
    for line1, line2 in zip(f1, f2):
      if line1 != line2:
        f1.close()
        f2.close()
        return False
  f1.close()
  f2.close()
  return True

"""
Delete all files ending in a suffix from a specific directory.
"""
def delete_files(dir, suffix):
  for file in os.listdir(dir):
    if file.endswith(suffix):
      path = os.path.join(dir, file)
      try:
        if os.path.isfile(path):
          os.remove(path)
      except Exception, e:
        print e

"""
Test count_frequency.
"""
def test_count_frequency():
  result = os.system("count_frequency samples/events2013.dat freqs2013.dat")
  assert_equal(0, result, "Unexpected return code")
  assert_true(os.path.isfile("freqs2013.dat"), "Could not find freqs2013.dat")
  actual = np.loadtxt("freqs2013.dat")
  expected = np.loadtxt("testoracle/freqs2013.dat")
  np.testing.assert_almost_equal(expected, actual, 2, \
                                 "freqs2013.dat not equal to testoracle/freqs2013.dat")

"""
Test count_frequency with a minimum token length.
"""
def test_count_frequency_minimum_token_length():
  result = os.system("count_frequency samples/events2013.dat freqs2013_5.dat 5")
  assert_equal(0, result, "Unexpected return code")
  assert_true(os.path.isfile("freqs2013_5.dat"), "Could not find freqs2013_5.dat")
  actual = np.loadtxt("freqs2013_5.dat")
  expected = np.loadtxt("testoracle/freqs2013_5.dat")
  np.testing.assert_almost_equal(expected, actual, 2, \
                                 "freqs2013_5.dat not equal to testoracle/freqs2013_5.dat")

"""
Test count_frequency with a missing output file name.
"""
def test_count_frequency_missing_output_file_name():
  result = os.system("count_frequency samples/events2013.dat")
  assert_not_equal(0, result, "Unexpected return code")
