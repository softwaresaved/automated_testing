# Regression Testing

By [Mike Jackson](https://www.software.ac.uk/about/people/mike-jackson), Software Sustainability Institute.

"Refactor, optimise and parallelise your code with confidence"

One of the risks of refactoring, optimising or parallelising our code is that we might introduce a bug as we do so.

We may not find these bugs until hours, days, or even weeks, later.

In this guide, I describe a recipe for introducing regression testing to enable us to quickly discover any bugs we might introduce when modifying our code.

## Overview

I start by describing why we need to test our code and why automated tests are an effective way to do so.

I then describe regression tests and a recipe for introducing regression tests for our code.

I walk through the recipe in detail, by means of a running example in Python, though the recipe can be applied within any language.

I also give examples of regression testing in practice from projects run at [EPCC](http://www.epcc.ed.ac.uk), The University of Edinburgh and [The Software Sustainability Institute](http://www.software.ac.uk). 

For the purpose of this guide, the term "code" can mean anything, whether this be C, C++, Fortran, or Java programs or Python, R, or bash scripts.

## Follow along...

If you want to run the examples in this guide yourself, then you will need Python 2.7 plus the [nose](https://pypi.python.org/pypi/nose/) test framework, and the [numpy](http://www.numpy.org/) scientific computing package. To download these, and other Python packages, the [Anaconda](https://store.continuum.io/cshop/anaconda/) all-in-one Python installer is recommended.

To get these examples, you can download the ZIP file of this repository by clicking on the Download ZIP button. Or, if know how to use Git, clone this repository, for example:
 
```
$ git clone http://github.com/softwaresaved/automated_testing.git
```

If using Linux/Unix, then, once you have the repository, we need to set permissions on a couple of scripts so they can be executed directly, and add the current directory to our PATH environment variable. Run the following:

```
$ chmod +x count_frequency
$ chmod +x test_count_frequency.sh
$ export PATH=.:$PATH
```

## Why test our code?

Why do we need to test our code? Consider the case of Geoffrey Chang, a researcher at the The Scripps Research Institute in the United States. In 2006, he and his colleagues retracted a number of papers from the journal Science. A bug in one of their codes meant that the data produced by this code was incorrect. As a result, the conclusions which they had drawn from this flawed data, were also incorrect.

> We wish to retract our research article ... and both of our Reports ... an in-house data reduction program introduced a change in sign ... converted the anomalous pairs (I+ and I-) to (F- and F+)...

Chang, G., Roth, C.B., Reyes, C.L., Pornillos, O., Yen-Ju, C., Chen, A.P. (2006) Retraction. Science 22 December 2006: Vol. 314 no. 5807 p. 1875  DOI: [10.1126/science.314.587.1875b](http://www.sciencemag.org/content/314/5807/1875.2.long)

It was a group of Swiss researchers that first raised concerns about the data. The data was flawed due to a bug in a data analysis program causing two columns to be flipped.

> Swiss researchers published a paper in Nature that cast serious doubt on a protein structure Chang's group had described in a 2001 Science paper.

> Chang was horrified to discover that a homemade data-analysis program had flipped two columns of data

Miller G. (2006) Scientific publishing. A scientist's nightmare: software problem leads to five retractions. Science 22 December 2006: Vol. 314 no. 5807 pp. 1856-1857 DOI: [10.1126/science.314.5807.1856](http://www.sciencemag.org/content/314/5807/1856.long)

Tests help us to help check that our code produces scientifically-correct results. 

Tests also help us to ensure that our code continues to do so when it is tidied, extended to support new functionality, bug-fixed, updated to use new libraries, optimised, and, parallelised.

After all, optimisation or parallelisation is futile if our code no longer works correctly, and we burn up our HPC resource budget running our incorrect code, and we don't notice until weeks, or months, later, or, another researcher notices before we do!

## Why automated tests?

Automated tests can be written once and then run many times, for example every day, or, every time we change our code.

What is a repetitive, manual process becomes an automated process, the sort at which computers excel.

Automation frees us to spend our time on innovative tasks, such as our research!

Refactoring, optimising and parallelising code without automated tests can be done, but it is like climbing without a rope, only for the brave and skilled!

## What type of automated tests?

The term automated testing sometimes makes people think of [unit tests](https://en.wikipedia.org/wiki/Unit_testing), testing the smallest units of our code, for example, functions, methods, sub-routines or classes. 

But, a challenge that we can face, especially if we have large, legacy codes, is, where to start?

The prospect of having to write dozens of unit tests can be off-putting at the best of times, let alone if we have data to analyse, a paper to write or a conference to prepare for.

Instead of starting with unit testing, we can start with [regression testing](https://en.wikipedia.org/wiki/Regression_testing). Regression testing allows us to check that our code continues to be correct after we have made changes to it. Unit testing can then be introduced at a later date, when the demands of research permit.

Regression testing does not test whether our code produces scientifically-correct results, only that we don't change its behaviour in unexpected ways. We will return to this distinction later.

## A recipe for introducing regression tests

To introduce regression testing we can follow a recipe.

* First, we create a [**test oracle**](https://en.wikipedia.org/wiki/Oracle_\(software_testing\)). We run out code on sets of input files and parameters. We save the corresponding output files. These output files serve as the **expected outputs** from our program given the corresponding input files and parameters.
* We then write **regression tests**. Each regression test runs our code for a set of input files and parameters. It then compares the output from our code to the expected outputs within the test oracle, it compares the **actual outputs** to the expected outputs.
* We **run** our regression tests regularly, or after every change to the code, to check we have not introduced any bugs that have changed its behaviour.

### EPCC oncology project 2009

As an example of regression testing in practice, let's look at [EPCC oncology project](http://www.hector.ac.uk/casestudies/oncology.php) from 2009.

The Colon Cancer Genetics Group at the Western General Hospital, Edinburgh had a Fortran code to identify the relationship between pairs of genetic markers and colorectal cancer. Researchers wanted to run their code on a data set of over 560,000 genetic markers with data from almost 2000 people. They estimated that it would take their code 400 days to process this data, so they asked EPCC to help optimise and parallelise their code so it could be run on the HECToR super-computer.

To ensure that their changes did not introduce any bugs, EPCC used regression testing. The code was run on a subset of the data to create a test oracle.  A set of regression tests were written. The code was then optimised and parallelised in stages, with the regression tests being run nightly to ensure that the behaviour of the code had not changed. After optimisation and parallelisation, the code was run with the full data set on 512 processors on HECToR. The run time was 5 hours.

I will now describe how to implement the recipe for regression testing by means of a running example in Python, though the recipe can be applied within any language.

## Implementing the regression test recipe

I will now describe how to implement the recipe for regression testing by means of a running example in Python, though the recipe can be applied within any language.

### Some assumptions about our code

In demonstrating how to apply the recipe, we will make a few assumptions about our code.

* We will assume that a user can run our code from the Linux or Unix shell or the DOS command prompt.
* We will assume it runs in batch mode, that is, once started it runs to completion without further user interaction. The code is configured via command-line parameters and/or configuration files and reads in zero or more input files.
* We will also assume that our code writes one or more output files and, optionally, exits with an [exit status](http://en.wikipedia.org/wiki/Exit_status) which indicates whether the code succeeded or failed in its operation. I say 'optionally' as some codes always return zero. 

There are many codes which have these qualities including C, C++, Fortran, and Java executables, and Python, R, and bash scripts.

### A token frequency program

As an example of a code that conforms to these assumptions, we will use a code that counts the frequency of numerical tokens - strings that represent integers or floating-point values - within a text file full of such tokens.

The code is called `count_frequency` and can be run under Linux, Unix or DOS.

It takes in two mandatory command-line arguments, an input file name and an output file name.

```
$ count_frequency INPUT_FILE OUTPUT_FILE [MINIMUM_TOKEN_LENGTH]
```

It reads in the input file, counts the frequency of each unique numerical token, and outputs a file with the frequency counts.

The output file has one row for each unique token.

```
# Frequency data
# Format: token count percentage
TOKEN FREQUENCY PERCENTAGE
. . .
```

Each row consists of the token, the number of occurrences of that token in the input file, and this number expressed as a percentage of the total number of unique tokens in the input file.

```
$ cat samples/events2013.dat:
6567
7831
6149
. . .

$ count_frequency samples/events2013.dat freqs_events2013.dat

$ cat freqs_events2013.dat
# Frequency data
# Format: token count percentage
2399 136 0.0136
8295 135 0.0135
8100 135 0.0135
. . .
```

The code also takes an optional command-line argument, the minimum length of a token. If this argument is provided, then only tokens of that length or longer are processed.

```
$ count_frequency samples/events2013.dat freqs5_events2013.dat 5

$ cat freqs5_events2013.dat
# Frequency data
# Format: token count percentage
10000 100 100.0
```

### Choose a language for regression tests

We need to choose a language in which to write our regression tests. As we assume our code can be run from the command-line, in batch mode, and, as we are writing regression tests, we are not restricted to using the implementation language of our code.

Which language do we choose?

Many languages provide functions that allow commands to be passed to the operating system, such as that to run our code. These functions also return the exit status from the commands run. Many languages also provide functions to check that directories and files exist, read in files line-by-line, parse lines and to compare values of various types, for example, integers, floats, doubles, strings, or booleans.

Many of these languages have associated [unit testing frameworks](http://en.wikipedia.org/wiki/xUnit). For example, C has CUnit, C++ has CppUnit and googletest, Fortran has FRUIT, Java has JUnit, Python has nose and py.test, and R has testthat (see, for example, The Software Sustainability Institute's [Build and test examples](http://github.com/softwaresaved/build_and_test_examples)).

Unit test frameworks provide numerous functions to help write tests. These include functions to compare values of various types, and to check whether certain conditions hold that mean that a test has passed or failed. They also record which tests pass and fail, and create reports summarising test passes and failures. Despite their name, unit test frameworks are not just for unit tests!

If we are new to a research project, we may not be familiar with the language used to implement the research code, so, we might choose a language that is easier for us to use, or with which we have the most experience.

We could choose a language which has a more powerful, or usable, test framework than those available within the code's implementation language.

Or, we might want to use the same language as our code, as this can make introducing unit tests in future less challenging.

For our example, we'll use Python, as it does not need to be compiled, and is complemented by two useful tools, the [nose](https://nose.readthedocs.org/) unit test framework, and the [numpy](http://www.numpy.org/) scientific computing package, which provides useful functions for comparing files with numerical data.

### Create a test oracle

Following the recipe, we first create a test oracle. We can create a directory, `testoracle`.

```
$ mkdir testoracle
```

We then run `count_frequency` on valid input files - those we know to be correct - and populate the `testoracle` directory with the corresponding output files.

```
$ count_frequency samples/events2013.dat testoracle/freqs_events2013.dat
$ count_frequency samples/events2013.dat testoracle/freqs5_events2013.dat 5
```

If we have many files we could use some form of automation, for example, a bash script, [create_test_oracle.sh](./create_test_oracle.sh):

```
for F in $(ls samples)
do
    count_frequency samples/$F testoracle/freqs_$F
    count_frequency samples/$F testoracle/freqs5_$F 5
done
```

Or a DOS script, [create_test_oracle.bat](./create_test_oracle.bat):

```
for /r %%F in (samples\*) do (
    count_frequency samples\%%~nxF testoracle\freqs_%%~nxF
    count_frequency samples\%%~nxF testoracle\freqs5_%%~nxF 5
)
```

We might even write a Makefile.

The more examples in our test oracle the better!

### Run our code

We now want to write a regression test. Firstly, it needs to run our code.

Python's [subprocess.call](https://docs.python.org/2/library/subprocess.html#subprocess.call) function allows commands to be passed to the operating system and run.

```
import subprocess

cmd = "count_frequency samples/events2013.dat freqs_events2013.dat"
subprocess.call(cmd, shell=True)
```

Setting `shell` to `True` tells Python to pass the command straight to the operating system.

We can write a simple Python script, `test_counts.py`, to run `count_frequency` using the `call` function. We can then run our script using Python.

```
$ python test_counts.py
```

By running our script, we run our code.

Most languages support functions like `call`. For example:

* C and C++ provide a [system](http://linux.die.net/man/3/system) function.
* Fortran provides a [SYSTEM](https://gcc.gnu.org/onlinedocs/gfortran/SYSTEM.html) subroutine.
* Java provides a [java.lang.Runtime](http://docs.oracle.com/javase/7/docs/api/java/lang/Runtime.html) class.
* Python provides a [subprocess](https://docs.python.org/2/library/subprocess.html) package
* R provides a [system2](https://stat.ethz.ch/R-manual/R-devel/library/base/html/system2.html) function.

### Create a test function

As we will have more than one regression test, we can put our test code within a function, for example, `test_count_frequency`.

```
import subprocess

def test_count_frequency():
  cmd = "count_frequency samples/events2013.dat freqs_events2013.dat"
  subprocess.call(cmd, shell=True)
```

Putting our test code into functions not only is more modular, it allows us to run our tests using a unit test framework.

The Python unit test framework, nose, has a test runner, `nosetests`, which looks for functions with the prefix `test_` and runs these. It records which tests succeeded and which failed, and prints reports on these.

If we run `test_counts.py` using `nosetests`, we get a report that shows our test successfully passed, as `nosetests` prints a dot for each test function that it finds and runs, and which succeeds.

```
$ nosetests test_counts.py
.
----------------------------------------------------------------------
Ran 1 test in 10.576s
OK
```

Many unit test frameworks provide these capabilities, so long as tests are written in a certain way. For example, using FRUIT for Fortran we write test subroutines.

```
! FORTRAN FRUIT example
subroutine test_count_frequency() . . .
```

Using JUnit for Java, we write test classes, and mark up test methods with annotations.

```
// Java JUnit example
import org.junit.Test;
public class CountFrequencyTest 
{
    @Test
    public void testCountFrequency() 
    {
        . . . 
    }
}
```

### Check exit status

Python's `call` function returns the exit status from the command that was passed to the operating system.

Linux, Unix and Windows adopt the convention that a exit status of zero means that a command exited OK and non-zero means that some problem arose.

We can check that the exit status is zero. We can use a function provided by nose, `assert_equal`, which compares two values for equality, and, if they are not equal, records that the test has failed, along with an informative failure message.

```
import subprocess
from nose.tools import assert_equal

def test_count_frequency():
  cmd = "count_frequency samples/events2013.dat freqs_events2013.dat"
  result = subprocess.call(cmd, shell=True)
  assert_equal(0, result, "Unexpected exit status")
```

If a code always returns zero, due to the way it has been implemented, that's OK, as we will also do other checks.

### Check output files were created

The next check we can do is that we have an output file with the frequency counts. 

Python's [os.path.isfile](https://docs.python.org/2/library/os.path.html#os.path.isfile) function allows us to check if a file exists. We can check that the expected output file now exists, after running `count_frequency`.

We can use a function provided by nose, `assert_true`, which checks if a condition holds and, if not, records that the test has failed, along with an informative failure message.

```
import os.path
import subprocess
from nose.tools import assert_equal
from nose.tools import assert_true

def test_count_frequency():
  cmd = "count_frequency samples/events2013.dat freqs_events2013.dat"
  result = subprocess.call(cmd, shell=True)
  assert_equal(0, result, "Unexpected exit status")
  assert_true(os.path.isfile("freqs_events2013.dat"),
              "Could not find freqs_events2013.dat")
```

By checking that the output file exists, we can handle situations where code we are testing returns an exit status of zero, even if problems arise.

We now have about the simplest test we can run on our code - if we give it a valid input file does it produce an output file.

The test is quite basic as we have not checked the contents of the output file.

### Compare output files to test oracle via operating system

Rather than just checking if an output file exists, we really want to check whether the output file is the one we expect, that is, it matches the expected output file we have in our test oracle.

Under Linux or Unix, we can use `call` to invoke the `diff` command to compare the actual output file to the expected output file. We can provide the `-q` command-line flag to `diff` to suppress its output.

If `diff` returns an exit status of zero then the two files are equal. If it returns an exit status of non-zero, then the two files differ. We can use `assert_equals` to check that we do indeed get an exit status of zero, and, if not, then fail our test.

```
def test_count_frequency():
  cmd = "count_frequency samples/events2013.dat freqs_events2013.dat"
  result = subprocess.call(cmd, shell=True)
  assert_equal(0, result, "Unexpected exit status")
  assert_true(os.path.isfile("freqs_events2013.dat"),
              "Could not find freqs_events2013.dat")
  cmd = "diff -q freqs_events2013.dat testoracle/freqs_events2013.dat"
  result = subprocess.call(cmd, shell=True)
  assert_equal(0, result, "freqs_events2013.dat =/= testoracle")
```

Under Windows, we can use the DOS `fc`, file compare, command, redirecting the output to `NUL` to suppress its output.

```
fc freqs_events2013.dat testoracle/freqs_events2013.dat > NUL
```

One problem with using `diff` or `fc` is that it makes our regression tests operating system dependent.

### Compare output files to test oracle in-code

We can make our regression tests operating system independent by comparing the actual output file to the test oracle's expected output file, within our test code. We add a function that compares two files line-by-line.

```
def compare_files(file_name1, file_name2):
  with open(file_name1) as file1, open(file_name2) as file2:
    for line1, line2 in zip(file1, file2):
      if line1 != line2:
        file1.close()
        file2.close()
        return False
  file1.close()
  file2.close()
  return True

def test_count_frequency():
  result = subprocess.call(
    "count_frequency samples/events2013.dat freqs_events2013.dat",
    shell=True)
  assert_equal(0, result, "Unexpected exit status")
  assert_true(os.path.isfile("freqs_events2013.dat"), 
              "Could not find freqs_events2013.dat")
  assert_true(compare_files("freqs_events2013.dat",
                            "testoracle/freqs_events2013.dat"),
              "freqs_events2013.dat =/= testoracle")
```

Even if we don't care about cross-platform portability, there are other good reasons why we should write code to check the correctness of our output files against the test oracle, as we will soon see.

If our chosen language has a library for comparing files, then we should use that instead.

### Add more tests

We now have a regression test.

Ideally, we'd want to add some, a lot, more tests, for example, to test `count_frequency` with a minimum token length.

```
def test_minimum_token_length():
  cmd = "count_frequency samples/events2013.dat freqs5_events2013.dat 5"
  result = subprocess.call(cmd, shell=True)
  assert_equal(0, result, "Unexpected exit status")
  assert_true(os.path.isfile("freqs5_events2013.dat"),
              "Could not find freqs5_events2013.dat")
  assert_true(compare_files("freqs5_events2013.dat",
                            "testoracle/freqs5_events2013.dat"),
              "freqs5_events2013.dat not equal to testoracle")
```

Another type of test we can do is to check what happens when our code is not given valid inputs. For example, if we do not provide an output file name to `count_frequency`, then it returns a non-zero exit status. We can write a regression test for this too.

```
from nose.tools import assert_not_equal

def test_missing_output_file_name():
  cmd = "count_frequency samples/events2013.dat"
  result = subprocess.call(cmd, shell=True)
  assert_not_equal(0, result, "Unexpected exit status")
```

After all, if changing `count_frequency`, we would not want to introduce a bug that means it returns an exit status of zero, if the output file name is not provided.

### EPCC and Farr Institute 2015

We now have a set of regression tests that run a code then compare the output files, line-by-line, to output files held within a test oracle. This type of regression testing was used by EPCC, as part of work with the [Farr Institute](http://www.farrinstitute.org/), which is building a secure platform for medical research.

A data linker was developed in Java to anonymise data before it is passed to researchers. The linker reads in mappings from data tokens to anonymised tokens, then reads data files and replaces occurrences of the data tokens with the corresponding anonymised tokens. A prototype had been developed, but needed improvements to its scalability and robustness.

A test oracle was created from a sample mapping file and data files.

The [Apache ANT](http://ant.apache.org/) build tool was used to develop a basic regression test framework. It ran the linker using ANT's support for invoking Java programs. It then checked that the anonymised output files existed, using an ANT function for this. It then compared the anonymised output files to those of the test oracle, calling a Java program to compare the files line-by-line.

## Comparing actual outputs to expected outputs

We will now look at the problems that can arise when comparing the actual outputs from our code against our expected outputs, and how to solve these problems.

### What is equality?

Comparing files line-by-line was OK for Farr, as its input and output files were sets of string tokens. In other research domains, comparing files in this way will not work.

For example, imagine we have a data file in [JSON](http://www.json.org/) format, which has a time-stamped log of events.

```
{"2015-01-06":{"Paused":"00:00:00"},"2015-01-07":{"Running":"00:00:00"},"2015-01-08":{"Paused":"15:48:00"},"2015-01-09":{"Paused":"15:48:00","Running":"03:34:00"}}
```

Now take this data, still in JSON format, but restructure it to be human-readable.

```
{
  "2015-01-06":{
    "Paused":"00:00:00"
  },
  "2015-01-07":{
    "Running":"00:00:00"
  },
  "2015-01-08":{
    "Paused":"15:48:00"
  },
  "2015-01-09":{
    "Paused":"15:48:00",
    "Running":"03:34:00"
  },
}
```

Both these files contain the same data, they are semantically equivalent. 

However, if we run the `diff` command, they are considered to be different due to the extra white-space in the human-readable version.

```
$ diff -q json/machine_readable.jsn json/human_readable.jsn
Files json/machine_readable.jsn and json/human_readable.jsn differ
```

Likewise, if we load them within an interactive Python session and compare them, they are different.

```
$ python
>>> machine = open("json/machine_readable.jsn").read()
>>> human = open("json/human_readable.jsn").read()
>>> machine == human
False
```

However, we can load them using Python's [json.loads](https://docs.python.org/2/library/json.html#json.loads) function, which loads a JSON file and uses it to populate a Python data structure called a [dictionary](https://docs.python.org/2/tutorial/datastructures.html#dictionaries).

```
>>> import json
>>> machine_json = json.loads(machine)
>>> human_json = json.loads(human)
```

If we then compare these dictionaries, we can see they that they are, indeed, equal.

```
>>> machine_json == human_json
True
```

If we refactor our code to output data files in a more human-readable format, by introducing white-space and newlines, then we want our regression tests to view these files as equivalent to their non-human readable counterparts, since their content is identical, only their presentation has changed. 

In this example, the Python `json.loads` function takes care of that for us. In other situations, we may have to write our own code to parse files and compare them for equality in the way we wish.

For example, imagine if we had data files that include a time-stamp recording information about when the data was created.

```
DateCreated: 2015-01-28 17:34
```

```
DateCreated: 2015-11-11 09:21
```

A string-based comparison for equality would fail, as our output files and test oracle files would have different time-stamps. 

In this scenario, we would want to have a smarter check for equality, one that:

* Checks that the line that is meant to hold the timestamp starts with the string `DateCreated`.
* Then, checks that its value is a valid time-stamp, without worrying about the exact date and time.


```
from datetime import datetime
from nose.tools import assert_true

def check_timestamp(date_created):
  assert_true(date_created.startswith("DateCreated: "), 
              msg="Invalid timestamp prefix " + date_created)
  try:
    date_str = date_created.strip("DateCreated: ")
    datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    is_valid = True
  except ValueError:
    is_valid = False
  assert_true(is_valid, "Invalid timestamp")

check_timestamp("DateCreated: 2015-01-28 11:23")
```

Again, we need to decide, given the nature of our data, and our research, what it means for data to be considered equal.

### Compare numerical values not strings

Returning to our example, `count_frequency` outputs data files which contain three columns of data. Two of these columns are integers and one is of floating point values. We want to compare our actual output file data to our expected output file data as numbers, and not strings. This is because the string `0` does not equal the string `0.0`, but the floating point value 0 does equal the floating point value 0.0.

Some languages have libraries that save us from having to write some, or all, of the code we might need to compare two files with numerical data.

For example, Python's scientific computing library, [numpy](http://www.numpy.org/), has functions that allow numerical data files to be compared for equality. Other languages have similar libraries.

numpy's `loadtxt` function loads a file assumed to contain numerical data. It skips any lines beginning with hash (`#`), as it treats these as comments.

We can use `loadtxt`, instead of our own `compare_files` function, and it will load the files into numpy arrays of numerical data.

numpy has functions to support tests that use multi-dimensional data. We can use one of these, `assert_equal`, to check that our actual values match our expected values. `assert_equal` checks that the data is equal both in terms of its dimensions, its number of rows and columns, and its actual values.

We add:

```
import numpy as np
```

and replace:

```
  assert_true(compare_files("freqs_events2013.dat",   
              "testoracle/freqs_events2013.dat"), 
              "freqs_events2013.dat =/= testoracle")
```

with:

```
  actual = np.loadtxt("freqs_events2013.dat")
  expected = np.loadtxt("testoracle/freqs_events2013.dat")
  np.testing.assert_equal(expected,
                          actual,
                          "freqs_events2013.dat =/= testoracle")
```

### When 0.1 + 0.2 does not equal 0.3

There is one further complication with our data that we need to address. EPCC's oncology project found that their regression tests failed when they ran their code on the HECToR super-computer. Investigation showed that this arose due to their floating point calculations giving subtly different results when run on their development machine compared to when they were run on HECToR. To see why these differences arose, look at this Python example.

If we assign 0.1 to `a` and 0.2 to `b` and print their sum, we get 0.3, as expected.

```
>>> a = 0.1
>>> b = 0.2
>>> print(a + b)
0.3
```

If, however, we compare the result of comparing the sum of `a` plus `b` to 0.3 we get `False`.

```
>>> print(a + b == 0.3)
False
```

If we show the value of `a` plus `b` directly, we can see there is a subtle margin of error.

```
>>> a + b
0.30000000000000004
```

This is because floating point numbers are approximations of real numbers.

The result of floating point calculations can depend upon the compiler or interpreter, processor or system architecture and number of CPUs or processes being used. 

Floating point calculations are not always guaranteed to be associative. A plus B will not necessarily equal B plus A.

### Equality in a floating point world

When comparing floating point numbers for equality, we have to compare to within a given tolerance, alternatively termed a threshold or delta. For example, we might consider A equal to B if the absolute value of the difference between A and B is within the absolute value of our tolerance.

A = B if | A - B <= | tolerance |

Many unit test frameworks provide functions for comparing equality of floating point numbers to within a given tolerance.

nose provides a function, `assert_almost_equal`, which compares two values for equality to within a given number of decimal places. For example, here is a test to compare two values.

```
>>> from nose.tools import assert_almost_equal
>>> expected = 2.000001
>>> actual = 2.0000000001
>>> assert_almost_equal(expected, actual, 0)
>>> assert_almost_equal(expected, actual, 2)
>>> assert_almost_equal(expected, actual, 4)
>>> assert_almost_equal(expected, actual, 6)
...
AssertionError: 2.000001 != 2.0000000001 within 6 places
```

This test passes if we compare these two values to within 0, 2 or 4 decimal places, but fails if we compare them to within 6 decimal places.

Unit test frameworks for other languages provide similar functions:

* Cunit for C: `CU_ASSERT_DOUBLE_EQUAL(actual, expected, granularity)`
* CPPUnit for C++: `CPPUNIT_ASSERT_DOUBLES_EQUAL(expected, actual, delta)`
* googletest for C++: `ASSERT_NEAR(val1, val2, abs_error)`
* FRUIT for Fortran: `subroutine assert_eq_double_in_range_(var1, var2, delta, message)`
* JUnit for Java: `org.junit.Assert.assertEquals(double expected, double actual, double delta)`
* testthat for R: 
  - `expect_equal(actual, expected, tolerance=DELTA)` - absolute error within `DELTA`
  - `expect_equal(actual, expected, scale=expected, tolerance=DELTA)` - relative error within `DELTA`

### Floating point values and our code

The third column of `count_frequency`'s output file is a column of floating point values, representing the number of occurrences of a tokens as a percentage of the total number of tokens in the input file. 

To ensure we don't run into problems due to floating point comparisons, we want to compare equality of our expected and actual output files, to within a given tolerance.

numpy also provides functions to compare multi-dimensional arrays to within a given tolerance. We can use one of these, `assert_equal`, to check that our actual frequencies match our expected frequencies.

We replace:

```
  actual = np.loadtxt("freqs_events2013.dat")
  expected = np.loadtxt("testoracle/freqs_events2013.dat")
  np.testing.assert_equal(expected,
                          actual,
                          "freqs_events2013.dat =/= testoracle")
```

with:

```
  actual = np.loadtxt("freqs_events2013.dat")
  expected = np.loadtxt("testoracle/freqs_events2013.dat")
  np.testing.assert_almost_equal(expected,
                                 actual,
                                 2,
                                 "freqs_events2013.dat =/= testoracle")
```

To see why this might be useful in our example, suppose we rewrote `count_frequency` so it could run in parallel. A parallel version of `count_frequency` could:

* Divide up the input file into a number of chunks, where a chunk might be, for example, 100 lines.
* It could then calculate, in parallel, the frequencies of tokens within each chunk.
* Then it would combine the results from each chunk to get the final frequencies.

As a result of our parallelisation, or any other optimisations, we might get subtle differences in our output files, in the column of percentages, that would then cause problems when matching these to our test oracle. 

So, we have talked about tolerance, what is a suitable tolerance, what is a suitable threshold for equality? That depends upon the domain, and the research being undertaken. For some fields, rounding to the nearest whole number may be acceptable. For others, far greater precision may be required.

## Regression testing examples

We will now will look at an another example of a regression test framework for `count_frequency`, but written in R, before looking at other examples of regression testing in practice.

## What our regression test framework does

We now have a regression test framework for `count_frequency` with three regression tests.

The first two tests check `count_frequency`'s behaviour when given a valid input file. They run `count_frequency` with both valid input files and command-line parameters, and check `count_frequency` exits with an exit status of zero, indicating success. They check that an output file exists, then compare the output file to the expected output file in the test oracle for equality, to within a given tolerance.

The third test checks `count_frequency`'s behaviour when not given an input file. It runs `count_frequency` and checks that `count_frequency` exits with a non-zero exit status, indicating an expected error.

### A regression test in R

As an example of how the recipe can be used with other languages, here is our first regression test, written in R, [test_count_frequency.R](./test_count_frequency.R):

```
library(testthat)

test.tolerance <- 1e-2

context("count_frequency tests")

test_that("Test count_frequency", {
  cmd <- "count_frequency"
  args <- "samples/events2013.dat freqs_events2013.dat"
  result <- system2(cmd, args)
  expect_equal(0, result, info="Unexpected exit status")
  expect_true(file.exists("freqs_events2013.dat"),
              info="Could not find freqs_events2013.dat")
  expected <- read.table("testoracle/freqs_events2013.dat",
                         stringsAsFactors=FALSE,
                         colClasses=("numeric"))
  actual <- read.table("freqs_events2013.dat",
                       stringsAsFactors=FALSE,
                       colClasses=("numeric"))
  expect_equivalent(dim(expected),
                    dim(actual),
                    info="Dimensions of freqs_events2013.dat not equal to testoracle")
  expect_equal(expected,
               actual,
               tolerance=test.tolerance,
               info="freqs_events2013.dat not equal to testoracle")
})
```

It uses functions from R's [testthat](http://cran.r-project.org/web/packages/testthat/index.html) unit test framework.

It assumes we have populated a `testoracle` directory, as we described earlier.

It uses R's [system2](https://stat.ethz.ch/R-manual/R-devel/library/base/html/system2.html) command to invoke `count_frequency`.

It uses testthat's `expect_equal` function to check the exit status from `count_frequency`.

It then uses testthat's `expect_true` and R's `file.exists` functions to check that the output file exists.

R's `read.table` function is used to read in the expected data from the test oracle and the actual data from the output file.

testthat's `expect_equivalent` function is used to compare the dimensions, the number of rows and columns, of the expected and actual data.

Finally, testthat's `expect_equal` function is used to compare the expected and actual data to within a given tolerance.

If you have R you can install testthat on Windows via: 

```    
> Rterm
```

and Linux/Unix via:

```
$ R
```

Run:

```
> install.packages("testthat")
> library(testthat)
CTRL-D
```

You can then run the tests as follows:

```
$ Rscript testthat.R
```

### FABBER

As another example of regression testing in practice, let's look at [FABBER](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FABBER).

FABBER is a C++ code developed by the University of Oxford to process medical images, and to help the recognition of blood flow patterns in the brain and to measure brain activity. It is invoked from within a set of shell scripts called BASIL.

The Software Sustainability Institute were asked to [propose how FABBER could be redesigned to be more modular and extensible](http://www.software.ac.uk/blog/2014-10-17-magnetic-imaging-software-now-fabberlously-easy-use)

As part of this work, one of their consultants did some rapid prototyping to demonstrate their suggestions, but, to ensure they didn't introduce any bugs, the consultant developed a regression test framework.

The consultant edited the BASIL shell scripts that invoked FABBER, so they could capture the input files and command-line parameters passed into FABBER from BASIL, and, likewise, to capture the output files from FABBER.

The consultant then worked through BASIL tutorials that invoked FABBER, so they could capture sets of input files, command-line parameters and output files. These then served as the test oracle.

The consultant used a shell script-based regression test framework that checked for the existence of output files, and compared expected files to actual files using the `diff` command.

One reason for the consultant using a regression test framework is that they were not a bioinformatician. There was no way they could assess the scientific correctness of FABBER’s outputs, but the regression test framework meant that they could detect whether or not they had changed its behaviour.

### TPLS (Two-phase Level Set)

[TPLS](http://sourceforge.net/projects/tpls/), Two-phase Level Set, from The University of Edinburgh and University College Dublin is an innovative Fortran code for modelling complex fluid flows, and which provides effective computational fluid dynamics analysis for academia and industry. TPLS runs on both Linux clusters and on the [ARCHER](http://www.archer.ac.uk) super-computer.

The Software Sustainability Institute [worked with TPLS](http://software.ac.uk/blog/2014-11-07-improved-code-archer-hits-target) to make it more usable and configurable. To ensure that no bugs were introduced during this refactoring, the Institute's consultant created a test oracle by running TPLS with sets of input parameters and saving its output files. TPLS has no input files.

A regression test framework was written in Python, using numpy, to compare TPLS output files to those of the test oracle. As the output files contained logging-related meta-data, these parts of the files were compared only in terms of the number of lines they had. The numerical data was compared using a numpy function, `numpy.allclose`, that, like `assert_almost_equal` compares multi-dimensional data for equality to within a given tolerance. This was essential given that TPLS produces subtly different results depending on the number of processors it runs on, or whether it is running on a Linux cluster or ARCHER.

## Conclusions

To conclude, I'll describe ways in which the regression test recipe can be customised, discuss some of its limitations and sum up key points of this guide.

### Customise the recipe

What I have presented is a recipe, not a set of hard-and-fast rules. It can to be customised to the needs of testing individual codes.

In our example, we are running the code we are testing as part of the regression test framework. In many cases, this will not be possible. For example, TPLS is run on ARCHER via ARCHER's job submission system. To invoke this from within Python would make the regression test framework unnecessarily complex. For TPLS, the regression test framework implemented the comparisons between the expected output data files of the test oracle and the actual output data files from a run of TPLS. A developer was required to run TPLS to create the actual output data files, before running the regression test framework.

Likewise, if we wanted to introduce regression tests for interactive or graphical-user interface-based programs, a similar approach could be adopted. A developer could follow a manual test script to create the output data files, then a regression test framework could be run to compare these to the test oracle.

As we saw for EPCC's oncology project, using a complete data set may be unfeasible. We may want to use a subset of our data, or a simplified data set, to create a test oracle. 

As an alternative to creating the test oracle from running our code, we can create the test oracle from experimental data. Or, we might want to use analytical solutions, results we have computed mathematically. This can be useful when implementing new algorithms from scratch, as it ensures that our code produces, and continues to produce, the expected results.

### Limitations

Regression testing does have some limitations. It does not test each individual function, method or class, only the code as a whole. To test these individually is the remit of unit tests.

Nor are regression tests guaranteed to test all parts of the code. Test coverage tools can provide information on what parts of our code are, or are not, executed when we run our regression tests.

Most importantly, regression tests do not test scientific correctness. This the remit of unit and system tests, though regression tests can serve as the starting point for introducing tests for scientific correctness, by both the use of analytical solutions within a test oracle, and test functions which read output files and check the data for scientific correctness, as defined by a researcher.

Regression tests also can serve as a starting point for introducing unit tests. When working with FABBER, the consultant added C++ code to log the input values to and return values from FABBER's C++ functions. They then ran the FABBER code, via the BASIL tutorials, and wrote unit tests in CppUnit to call these functions with the input values that had been logged, and to check that the return values were equal to the return values that had been logged. Removing the logging code restored FABBER to its original state, and the consultant was left with an initial set of unit tests for some of FABBER's functions.

### Key points

Automated tests can be written just once, but run many times, freeing us up to focus on innovative activities, such as research! In this guide, I presented a recipe to introduce regression tests:

* Create a test oracle with our expected outputs for sets of input files and parameters.
* Write regression tests which run our code, and compares the actual outputs to the expected outputs of the test oracle.
* And, run the regression tests regularly or after every change to the code.

Regression tests can help new developers on research projects, developers who know how to develop, refactor and optimise code but may lack the domain knowledge required to validate that the outputs are scientifically correct.

If a researcher validates the outputs used to create the test oracle, then a developer can develop, refactor, and optimise the code, with confidence that they are not undermining its scientific correctness.

Regression tests provide us with a way to ensure that when we refactor, fix, extend, tidy, optimise or parallelise our code we do not accidently introduce a bug as we do so, and, if we do introduce a bug, then to help us to spot this quickly.

They act as a valuable safety net for our development.

## Acknowledgements, copyright and licence

Copyright (c) 2014-2015 The University of Edinburgh.

Code is licensed under the [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html) licence. The licence text is also in [LICENSE-2.0.txt](./LICENSE-2.0.txt).

Documents are licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en_US)

This guide draws upon ideas from, and materials developed by, the following:

* [Software Carpentry](http://software-carpentry.org), a non-profit volunteer organization whose members teach researchers basic software skills.
* [The Software Sustainability Institute](http://www.software.ac.uk) which cultivates better, more sustainable, research software to enable world-class research ("better software, better research").
* [ARCHER](http://www.archer.ac.uk), the UK National Supercomputing Service.
