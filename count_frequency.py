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

import sys

DELIMITERS = ". , ; : ? $ @ ^ < > # % ` ! * + - = ( ) [ ] { } / \" '".split()


def load_text(file_name):
    """
    Load lines from a plain-text file and return these as a list, with
    trailing newlines stripped.

    Arguments:
        file_name (str or unicode): file name.
    Returns:
        list of str or unicode: lines.
    """
    with open(file_name) as text_file:
        lines = text_file.read().splitlines()
    return lines


def save_token_counts(file_name, counts):
    """
    Save a list of [token, count, percentage] lists to a file, in the
    form "token count percentage", one tuple per line.

    Arguments:
        file_name (str or unicode): file name.
        counts (list of list of [str or unicode, int, double]):
        lists of form [token, count, percentage].
    """
    frequencies = open(file_name, 'w')
    frequencies.write("# Frequency data\n")
    frequencies.write("# Format: token count percentage\n")
    for count in counts:
        frequencies.write("%s\n" % " ".join(str(c) for c in count))
    frequencies.close()


def load_token_counts(file_name):
    """
    Load a list of (token, count, percentage) tuples from a file where
    each line is of the form "token count percentage". Lines starting
    with # are ignored.

    Arguments:
        file_name (str or unicode): file name.
    Returns:
        list of (str or unicode, float, double): tuples of form [token,
        count, percentage].
    """
    counts = []
    frequencies = open(file_name, "r")
    for line in frequencies:
        if not line.startswith("#"):
            fields = line.split()
            counts.append((fields[0], int(fields[1]), float(fields[2])))
    frequencies.close()
    return counts


def update_token_counts(line, counts):
    """
    Given a string, parse the string and update a dictionary of token
    counts (mapping tokens to counts of their frequencies). DELIMITERS
    are removed before the string is parsed. The function is
    case-insensitive and tokens in the dictionary are in lower-case.

    Arguments:
        line (str or unicode): line of text.
        counts (dict of str or unicode: int): map from tokens to
        frequency counts.
    """
    for purge in DELIMITERS:
        line = line.replace(purge, " ")
    tokens = line.split()
    for token in tokens:
        token = token.lower().strip()
        if token in counts:
            counts[token] += 1
        else:
            counts[token] = 1


def calculate_token_counts(lines):
    """
    Given a list of strings, parse each string and create a dictionary
    of token counts (mapping tokens to counts of their
    frequencies). DELIMITERS are removed before the string is
    parsed. The function is case-insensitive and tokens in the
    dictionary are in lower-case.

    Arguments:
        lines (list of str or unicode): lines of text.
    Returns:
        dict of str or unicode: int: map from tokens to frequency
        counts.
    """
    counts = {}
    for line in lines:
        update_token_counts(line, counts)
    return counts


def token_count_dict_to_tuples(counts, decrease=True):
    """
    Given a dictionary of token counts (mapping tokens to counts of
    their frequencies), convert this into an ordered list of tuples
    (token, count). The list is ordered by decreasing count, unless
    increase is True. For equal counts, the list is ordered by token.

    Arguments:
        counts (dict of str or unicode: int): map from tokens to
        frequency counts.
        decrease (bool): sort in decreasing, or increasing order.
    Returns:
        list of (str or unicode, int): tuples of form (token, count).
    """
    return sorted(counts.items(), key=lambda key_value: (key_value[1],
                                                         key_value[0]),
                  reverse=decrease)


def filter_token_counts(counts, min_length=1):
    """
    Given a list of (token, count) tuples, create a new list with only
    those tuples whose token is >= min_length.

    Arguments:
        counts (list of (str or unicode, int)): tuples of form (token,
        count).
        min_length (int): minimum length of token.
    Returns:
        list of (str or unicode, int): tuples of form (token, count)
        whose tokens have length >= min_length.
    """
    stripped = []
    for (token, count) in counts:
        if len(token) >= min_length:
            stripped.append((token, count))
    return stripped


def calculate_percentages(counts):
    """
    Given a list of (token, count) tuples, create a new list (token,
    count, percentage) where percentage is the percentage number of
    occurrences of this token compared to the total number of tokens.

    Arguments:
        counts (list of (str or unicode, int)): tuples of form (token,
        count).
    Arguments:
        list of (str or unicode, int, double): tuples of form (token,
        count, percentage).
    """
    total = 0
    for count in counts:
        assert count[1] >= 0
        total += count[1]
    tuples = [(token, count, (float(count) / total) * 100.0)
              for (token, count) in counts]
    return tuples


def token_count(input_file, output_file, min_length=1):
    """
    Load a file, calculate the frequencies of each token in the file
    and save in a new file the tokens, counts and percentages of the
    total in descending order. Only tokens whose length is >=
    min_length are included.

    Arguments:
        input_file (str or unicode): file name.
        output_file (str or unicode): file name.
        min_length (int): minimum length of token.
    """
    lines = load_text(input_file)
    counts = calculate_token_counts(lines)
    sorted_counts = token_count_dict_to_tuples(counts)
    sorted_counts = filter_token_counts(sorted_counts, min_length)
    percentage_counts = calculate_percentages(sorted_counts)
    save_token_counts(output_file, percentage_counts)


def print_usage():
    """
    Print usage information.
    """
    print("Usage: python count_frequency.py " +
          "INPUT_FILE OUTPUT_FILE [MINIMUM_LENGTH]")


def main(arguments):
    """
    Calculate frequency of occurrences of tokens in a text file.

    Arguments:
        arguments (list[str or unicode]): input file name, output file
        name, and, (optional) minimum length of token to find. If a
        minimum length is given then only tokens of width greater than
        or equal to this are considered.
    """
    num_args = len(arguments)
    if num_args == 1:
        print_usage()
        sys.exit(1)
    input_file = arguments[1]
    if num_args == 2:
        print_usage()
        sys.exit(2)
    output_file = arguments[2]
    min_length = 1
    if len(arguments) > 3:
        min_length = int(arguments[3])
    token_count(input_file, output_file, min_length)

if __name__ == '__main__':
    main(sys.argv)
