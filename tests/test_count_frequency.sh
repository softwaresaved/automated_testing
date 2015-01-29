#!/bin/sh

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

# count_frequency tests
#
# These tests expect:
# - count_frequency to be in the path or the current directory.
# - Input files to be in a samples/ directory:
#   - events2013.dat
# - Test oracle files to be in a testoracle/ directory:
#   - freqs2013.dat created via 
#     count_frequency samples/events2013.dat testoracle/freqs2013.dat
#   - freqs2013_5.dat created via 
#     count_frequency samples/events2013.dat testoracle/freqs2013.dat 5

# $1 - file to check existence for.
check_file_exists() {
  if [ -f "$1" ]
  then
    echo "."
  else
    echo "FAILURE: $1 not found"
  fi
}

# $1 - file to check non-existence for.
check_file_not_exists() {
  if [ -f "$1" ]
  then
    echo "FAILURE: $1 exists"
  else
    echo "."
  fi
}

# $1 - file to compare.
# $2 - file to compare.
check_files_equal() {
  diff -rq $1 $2
  if [ $? == 0 ]; then
    echo "."
  else
    echo "FAILURE: $1 does not equal $2"
  fi
}

# $1 - return code to check.
check_return_code_ok() {
  if [ $1 == 0 ]; then
    echo "."
  else
    echo "FAILURE: non-zero return code $1"
  fi
}

# $1 - return code to check.
check_return_code_not_ok() {
  if [ $1 == 0 ]; then
    echo "FAILURE: non-zero return code $1"
  else
    echo "."
  fi
}

# Remove any output files from previous test run.
rm -f *.dat

echo "Test count_frequency"
count_frequency samples/events2013.dat freqs2013.dat
check_return_code_ok $?
check_file_exists freqs2013.dat
check_files_equal freqs2013.dat testoracle/freqs2013.dat

echo "Test count_frequency with minimum token length"
count_frequency samples/events2013.dat freqs2013_5.dat 5
check_return_code_ok $?
check_file_exists freqs2013_5.dat
check_files_equal freqs2013_5.dat testoracle/freqs2013_5.dat

echo "Test count_frequency with missing output file name"
count_frequency samples/events2013.dat
check_return_code_not_ok $?
