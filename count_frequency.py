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

import datetime
import string
import sys

DELIMITERS=".,;:?$@^<>#%`!*-=()[]{}/\"\'"
TRANSLATE_TABLE = string.maketrans(DELIMITERS, len(DELIMITERS) * " ")

"""
Frequency count.

Usage:

@code
python count_frequency.py INPUT_FILE OUTPUT_FILE [MINIMUM_LENGTH]
@endcode

Read in INPUT_FILE, a text file, and output a tabular file,
OUTPUT_FILE with a header:

@code
# Frequency data
# Format: token count percentage
@endcode

followed by N rows, one row per each token in INPUT_FILE, each row
consisting of three elements:

- Token.
- Frequency of occurrence of the token in the file.
- Frequency as a percentage of the total number of tokens.

If MINIMUM_LENGTH is given then only tokens of width greater than or
equal to this are considered.
"""

"""
Load lines from a plain-text file and return these as a list, with
trailing newlines stripped.
"""
def load_text(file):
  text = ""
  with open(file) as f:
    lines = f.read().splitlines()
  return lines

"""
Save a list of [token, count, percentage] lists to a file, in the form
"token count percentage", one tuple per line.
"""
def save_token_counts(file, counts):
  f = open(file, 'w')
  f.write("# Frequency data\n")
  f.write("# Format: token count percentage\n")
  for count in counts:
    f.write("%s\n" % " ".join(map(str, count)))
  f.close()

"""
Load a list of (token, count, percentage) tuples from a file where each
line is of the form "token count percentage". Lines starting with # are
ignored.
"""
def load_token_counts(file):
  counts = []
  f = open(file, "r")
  for line in f:
    if (not line.startswith("#")):
      fields = line.split()
      counts.append((fields[0], int(fields[1]), float(fields[2])))
  f.close()
  return counts

"""
Given a string, parse the string and update a dictionary of token
counts (mapping tokens to counts of their frequencies). DELIMITERS are
removed before the string is parsed. The function is case-insensitive
and tokens in the dictionary are in lower-case.
"""
def update_token_counts(line, counts):
  line = string.translate(line, TRANSLATE_TABLE) 
  tokens = line.split()
  for token in tokens:
    token = token.lower().strip()
    if token in counts:
      counts[token] += 1
    else:
      counts[token] = 1

"""
Given a list of strings, parse each string and create a dictionary of
token counts (mapping tokens to counts of their frequencies). DELIMITERS
are removed before the string is parsed. The function is
case-insensitive and tokens in the dictionary are in lower-case.
"""
def calculate_token_counts(lines):
  counts = {}
  for line in lines:
    update_token_counts(line, counts)
  return counts

"""
Given a dictionary of token counts (mapping tokens to counts of their
frequencies), convert this into an ordered list of tuples (token,
count). The list is ordered by decreasing count, unless increase is
True.
"""
def token_count_dict_to_tuples(counts, decrease = True):
  return sorted(counts.iteritems(), key=lambda (key,value): value, \
    reverse = decrease)

"""
Given a list of (token, count) tuples, create a new list with only
those tuples whose token is >= min_length.
"""
def filter_token_counts(counts, min_length = 1):
  stripped = []
  for (token, count) in counts:
    if (len(token) >= min_length):
      stripped.append((token, count))
  return stripped

"""
Given a list of (token, count) tuples, create a new list (token, count,
percentage) where percentage is the percentage number of occurrences
of this token compared to the total number of tokens.
"""
def calculate_percentages(counts):
  total = 0
  for count in counts:
    assert count[1] >= 0
    total += count[1]
  tuples = [(token, count, (float(count) / total) * 100.0) 
    for (token, count) in counts]
  return tuples

"""
Load a file, calculate the frequencies of each token in the file and
save in a new file the tokens, counts and percentages of the total  in
descending order. Only tokens whose length is >= min_length are
included.
"""
def token_count(input_file, output_file, min_length = 1):
  lines = load_text(input_file)
  counts = calculate_token_counts(lines)
  sorted_counts = token_count_dict_to_tuples(counts)
  sorted_counts = filter_token_counts(sorted_counts, min_length)
  percentage_counts = calculate_percentages(sorted_counts)
  save_token_counts(output_file, percentage_counts)

"""
Print usage information.
"""
def print_usage():
      print "Usage: python count_frequency.py INPUT_FILE OUTPUT_FILE [MINIMUM_LENGTH]"

if  __name__ =='__main__':
  num_args = len(sys.argv)
  if (num_args == 1):
      print_usage()
      sys.exit(1)
  input_file = sys.argv[1]
  if (num_args == 2):
      print_usage()
      sys.exit(2)
  output_file = sys.argv[2]
  min_length = 1
  if (len(sys.argv) > 3):
    min_length = int(sys.argv[3])
  token_count(input_file, output_file, min_length)
