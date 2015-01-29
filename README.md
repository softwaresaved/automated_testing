# Adopting automated testing

Automated tests provide a way to check that research software both produces scientifically-valid results and that it continues to do so if it is extended, refactored, optimised or tidied. But, a challenge that can face researchers, especially those with large, legacy codes, is, where to start? The prospect of having to write dozens of unit tests can be off-putting at the best of times, let alone if one has data to analyse, a paper to write or a conference to prepare for. 

In this guide, we provide an example of how automated testing can be adopted to give researchers the security to refactor, extend, optimise or tidy, their code, but without the overhead of having to implement dozens of unit tests at the outset. Instead of starting with [unit testing](http://en.wikipedia.org/wiki/Software_testing#Unit_testing), we start with end-to-end, or [system testing](http://en.wikipedia.org/wiki/Software_testing#System_testing). Unit testing can then be adopted at a later date, when the demands of research permit.

## Approach

Our approach to introducing automated testing is to first run the software to be tested for sets of input files and command-line arguments, and save the output files. These output files serve as a [test oracle](http://en.wikipedia.org/wiki/Oracle_%28software_testing%29), a means of determining whether a test has passed or failed.

We then write automated tests that:

* Run the software for a set of input files and command-line arguments.
* Check the software's return code to see that it exited without any errors.
* Check that the expected output files were created.
* Check that the output files are equal to those of the test oracle that were created using the same combination of input files and command-line arguments.

## Assumptions about the software to be tested

We assume that the software to be tested has the following qualities:

* It can be run from the command-line, in batch mode. That is, the user can invoke the software from the Linux/Unix shell or Windows DOS prompt and once they press ENTER the software runs to completion without the need for further user interaction.
* It reads in zero or more input files.
* It supports zero or more command-line arguments.
* It outputs zero or more files.
* On completion, it returns an [exit status](http://en.wikipedia.org/wiki/Exit_status) or return code to the command prompt.

There are many software tools which have these qualities. We can exploit these qualities and treat the software as a standalone component, which takes some inputs (its files and command-line arguments) and produces some outputs (a return code and some output files). As we will see, in the approach we are taking to testing, the language used to implement the software e.g. C, C++, Fortran, Java, Python or R) does *not* matter.

## Example software

As an example, we will write automated tests for software that calculates the frequency of tokens (numbers or words) within a text file.

If you want to run this example yourself, then you will need Python 2.7 plus the [nose](https://pypi.python.org/pypi/nose/) test framework, and the [numpy](http://www.numpy.org/) scientific computing package. To download these, and other Python packages, the [Anaconda](https://store.continuum.io/cshop/anaconda/) all-in-one Python installer is recommended.

To get this example, you can download the ZIP file of this repository by clicking on the Download ZIP button. Or, if know how to use Git, clone this repository, for example:
 
    git clone http://github.com/softwaresaved/automated_testing.git

If using Linux/Unix, then, once you have the repository, run:

    chmod +x count_frequency
    chmod +x test_count_frequency.sh
    export PATH=.:$PATH

The software is called count_frequency and can be run as follows under both Linux/Unix and Windows:

    count_frequency INPUT_FILE OUTPUT_FILE

It reads in a text file, INPUT_FILE, and outputs a tabular file, OUTPUT_FILE, with a header

    # Frequency data
    # Format: token count percentage

followed by N rows, one row per each token in INPUT_FILE, each row consisting of three elements:

* Token.
* Frequency of occurrence of the token in the file.
* Frequency as a percentage of the total number of tokens.

For example, if we run:

    count_frequency samples/events2013.dat freqs2013.dat

freqs2013.dat would contain:

    # Frequency data
    # Format: token count percentage
    2399 136 0.0136
    8295 135 0.0135
    8100 135 0.0135
    2624 135 0.0135
    5208 133 0.0133
    3422 133 0.0133
    3435 132 0.0132
    3950 132 0.0132
    ...

If an additional numerical command-line argument is given then only tokens of length equal to or greater than that value are considered. For example, if we run:

    count_frequency samples/events2013.dat freqs2013.dat 5

freqs2013.dat would contain:

    # Frequency data
    # Format: token count percentage
    10000 100 100.0

## Choose a language for the tests

As we assume the software can be run from the command-line, in batch mode, and, as we are writing system tests, we are not restricted to using the implementation language of the software. Many languages (e.g. C, C++, Fortran, Java, Python, or shell scripts) support functions or commands that allow programs to be invoked on the command-line, return codes to be retrieved, the existence of directories and files to be verified, files to be read in line-by-line and values of various types (e.g. integers, floats, strings, booleans) to be compared.

Many of these languages have associated [xUnit](http://en.wikipedia.org/wiki/XUnit) testing frameworks. For example, CUnit for C, CppUnit and googletest for C++, FRUIT for Fortran, Junit for Java (see our [Build and test examples](https://github.com/softwaresaved/build_and_test_examples)). These provide myriad features to help with the writing of tests and, despite their name, are not restricted to unit tests. These features include commands and functions to compare values of various types, checking whether certain conditions hold that are required for a test to pass, recording when tests pass or fail, and creating reports summarising test passes and failures.

We can write tests in any language according to whichever criteria is important to us:

* If we are new to a research project we may not be familiar with the language used to implement the software. So, we could choose to use a language we are familiar with to write a set of tests before we start to make changes to the software and learn more about its implementation language.
* We could choose a language which has more powerful or usable testing frameworks than those available for the implementation language.
* We might just choose a language that is easier for us to use or with which we have more experience.

In our example, we'll use Python as it does not need to be compiled and is complemented by two useful tools, the [nose](https://pypi.python.org/pypi/nose/) xUnit test framework, and the [numpy](http://www.numpy.org/) scientific computing package, which provides useful functions for comparing data files.

## Create a test oracle

We will first create a test oracle. We can create a directory, testoracle, then run count_frequency on valid inputs and populate testoracle with the corresponding outputs. For example:

    count_frequency samples/events2013.dat testoracle/freqs2013.dat
    count_frequency samples/events2013.dat testoracle/freqs2013_5.dat 5
    count_frequency samples/events2014.dat testoracle/freqs2014.dat
    count_frequency samples/events2014.dat testoracle/freqs2014_5.dat 5
    count_frequency samples/events2015.dat testoracle/freqs2015.dat

## Write code that runs the software

Python's [os.system](http://docs.python.org/2/library/os.html#os.system) function allows commands to be passed to the operating system and run. So, we can run software from the command-line by creating a file, test_counts.py, and adding the following to it:

    import os

    os.system("count_frequency samples/events2013.dat freqs2013.dat")

We can run this and so run the software, as follows:

    python test_counts.py

## Write code that checks the return code

os.system returns the return code from the system call which can then be checked. Linux/Unix and Windows both adopt the convention that a return code of 0 means that the command exited OK and non-zero indicates an error. So, we can check that this is the case:

    import os
    from nose.tools import assert_equal

    result = os.system("count_frequency samples/events2013.dat freqs2013.dat")
    assert_equal(0, result, "Unexpected return code")

Here, we use Python's nose.tools.assert_equal function (which, behind the scenes just calls, [unittest.TestCase.assertEqual](https://docs.python.org/2/library/unittest.html#unittest.TestCase.assertEqual)). This function compares two values for equality and if they are not equal prints the given message.

## Write code that checks that the expected output files were created

Python's [os.path.isfile](https://docs.python.org/2/library/os.path.html#os.path.isfile) function checks if a file exists. So, we can check that the expected output file now exists:

    import os
    import os.path
    from nose.tools import assert_equal
    from nose.tools import assert_true
    
    result = os.system("count_frequency samples/events2013.dat freqs2013.dat")
    assert_equal(0, result, "Unexpected return code")
    assert_true(os.path.isfile("freqs2013.dat"), "Could not find freqs2013.dat")

Here, we use Python's nose.tools.assert_true function (which, behind the scenes just calls, [unittest.TestCase.assertTrue](https://docs.python.org/2/library/unittest.html#unittest.TestCase.assertTrue)). This function checks a boolean value and if it is false prints the given message.

By checking that the output files exist we handle the situation where our software might exit with a return code of 0 even if problems arose or no output files were produced.

This is about the simplest test we can run with the software - if we give it valid inputs it produces the expected output files.

## Write code that checks that the output files are equal to those of the test oracle

The above tests can help us to check, when working with our software, that we haven't introduced any drastic errors but it would be better if we actually checked the content of those output files to ensure that, when making our changes, we don't corrupt the behaviour of the software and it doesn't start to output nonsense in its output files. Under Linux/Unix shell we could use the diff command (with its -q flag to suppress its output) e.g.

    result = os.system("diff -q freqs2013.dat testoracle/freqs2013.dat")

For Windows could use the Windows DOS fc (file compare) command (using > NUL to suppress its output) e.g.

    result = os.system("fc freqs2013.dat testoracle/freqs2013.dat > NUL")

We could then check the return code from the comparison:

    assert_equal(0, result, "freqs2013.dat not equal to testoracle/freqs2013.dat")

While this approach works, it does make our test code operating system dependant. We can make it more portable by comparing the files within the language in which we are writing our tests. We can add a function that compares two files line-by-line:

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

    result = os.system("count_frequency samples/events2013.dat freqs2013.dat")
    assert_equal(0, result, "Unexpected return code")
    assert_true(os.path.isfile("freqs2013.dat"), "Could not find freqs2013.dat")
    assert_true(compare_files("freqs2013.dat", "testoracle/freqs2013.dat"), \
      "freqs2013.dat not equal to testoracle/freqs2013.dat")

Even if we don't care about cross-platform portability, there are other good reasons why we should write code to check the correctness of our output files against the test oracle.

## Let the language work for us

Some languages have libraries that save us from having to write some, or all, of our file comparison code. For example, Python's scientific computing library, [numpy](http://www.numpy.org/) consists of functions that allow numerical data files to be compared for equality. So we can replace:

    assert_true(compare_files("freqs2013.dat", "testoracle/freqs2013.dat"), \
      "freqs2013.dat not equal to testoracle/freqs2013.dat")

with:

    import numpy as np

    actual = np.loadtxt("freqs2013.dat")
    expected = np.loadtxt("testoracle/freqs2013.dat")
    np.testing.assert_equal(expected, actual, \
      "freqs2013.dat not equal to testoracle/freqs2013.dat")

[numpy.loadtxt](http://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html) loads a file assumed to contain numerical data. It skips the lines beginning with # by default, as it treats these as comments. [numpy.testing.assert_equal](http://docs.scipy.org/doc/numpy/reference/generated/numpy.testing.assert_equal.html) checks that the given data is equal in its dimensions (e.g. number of rows and columns) and its values.

## Exploit knowledge about the output data

Another advantage of checking our output files against our test oracle in-code is we can implement checks that exploit the knowledge of the data and how it is structured. For example, if our output data files included a time-stamp recording information about when the data was created e.g.

    DateCreated: 2015-28-01 17:34

then we'd want to exclude this from our comparisons with the output files in our test oracle, which would most likely have different time-stamps. Instead, we would check for the existence of this      DateCreated entry in the output files, and check that its value is a valid time-stamp.

### Decide what it means for output files to be equal

We may wish to distinguish between the form and content of our files. For example, the two [JSON](http://www.json.org/) files [json/machine_readable.jsn](./json/machine_readable.jsn) and [json/human_readable.jsn](./json/human_readable.jsn) contain the same information, only one is formatted to be more readable by us. That they are semantically equivalent can be seem if we load them into Python. We can create an interactive Python session and import Python's [json](https://docs.python.org/2/library/json.html) library:

    python
    >>> import json

Then we can load the files and copy their contents into strings:

    >>> machine=open("json/machine_readable.jsn").read()
    >>> human=open("json/human_readable.jsn").read()
    
The [json.loads](https://docs.python.org/2/library/json.html#json.loads) function can parse these strings into a Python data structure called a [dictionary](https://docs.python.org/2/tutorial/datastructures.html#dictionaries)):
   
    >>> machine_json=json.loads(machine)
    >>> human_json=json.loads(human)

And, if we now compare the dictionaries, we see they are equal:
    
    >>> machine_json.keys() == human_json.keys()
    True
    >>> machine_json.values() == human_json.values()
    True
    >>> machine_json == human_json
    True

If our test oracle contained machine readable versions of files, and we refactored our software, to output the data files in a more human-readable format by introducing white-space and newlines, then we want our automated tests to still view these files as equivalent since their content is identical, only their presentation has changed. In the above example, json.loads takes care of that for us, parsing the files into a data structure for us. In other situations, we may have to write the code that parses the files in such a way that we can compare their contents.

### Equality in a floating point world

Even if we do our checks in-code using numpy, as above, it is important to remember that computers don't do floating point computations that well. For example, consider this short Python session:

    >>> a = 0.1
    >>> b = 0.2
    >>> print a + b
    0.3
    >>> print a + b == 0.3
    False
    >>> a + b
    0.30000000000000004

Floating point numbers within a computer are approximations of real numbers. A complication arising from this is that floating point arithmetic is not guaranteed to be associative i.e. *(a + b) + c* will not necessarily equal *a + (b + c)*.

To see how this affects testing, suppose we rewrote count_frequency so it could run in parallel. A parallel version of count_frequency could:

* Divide up the input file into a number of chunks. For example a chunk may be 100 lines.
* Calculate, in parallel, the frequencies of tokens within each chunk.
* Combine the results from each chunk to get the final frequencies.

As a result of our parallelisation, or any other optimisations, we might get subtle differences in our output files that would then cause problems when matching these to our test oracle. For example, suppose the file [outputs/freqs2013.dat](./outputs/freqs2013.dat) was the output from our parallelised software, when run with samples/events2013.dat as its input file. If we compare this to our test oracle we see a problem:

    >>> import numpy as np
    >>> expected = np.loadtxt("testoracle/freqs2013.dat")
    >>> actual = np.loadtxt("outputs/freqs2013.dat")
    >>> np.testing.assert_equal(expected, actual)
    ...
    AssertionError:
    ...
    Arrays are not equal
    ...
    
When checking floating point values, we want to compare for equality *within a given threshold*. We accept that two values are equal if their values are "close enough" For example, given *a* and *b* we might accept that *a* equals *b* if to be equal if *abs(a) - abs(b) < 0.000000000001*.

Many languages have libraries, often as part of test frameworks, that provide functions for such floating point comparisons to be done. For example, nose provides the nose.tools.assert_almost_equal function (which, behind the scenes just calls [unittest.TestCase.assertAlmostEqual](https://docs.python.org/2/library/unittest.html#unittest.TestCase.assertAlmostEqual)). This function takes the values to be compared and a number of decimal places:

    >>> from nose.tools import assert_almost_equal
    >>> e = 2.000001
    >>> a = 2.0000000001
    >>> assert_almost_equal(e, a, 0)
    >>> assert_almost_equal(e, a, 2)
    >>> assert_almost_equal(e, a, 4)
    >>> assert_almost_equal(e, a, 6)
    ...
    AssertionError: 2.000001 != 2.0000000001 within 6 places

Using these functions we could load in our output file and our test oracle file and compare the values for "almost equality" on a pair-by-pair basis. However, Python's numpy library has a function, [numpy.testing.assert_almost_equal](http://docs.scipy.org/doc/numpy/reference/generated/numpy.testing.assert_almost_equal.html) which checks that the given data matches to within a set number of decimal places. For example:

    >>> np.testing.assert_equal(expected, actual)
    Arrays are not equal
    >>> np.testing.assert_almost_equal(expected, actual, decimal=4)
    Arrays are not almost equal to 4 decimals
    >>> np.testing.assert_almost_equal(expected, actual, decimal=3)
    Arrays are not almost equal to 3 decimals
    >>> np.testing.assert_almost_equal(expected, actual, decimal=2)

numpy also provides [numpy.testing.assert_allclose](http://docs.scipy.org/doc/numpy/reference/generated/numpy.testing.assert_allclose.html) which provides an alternative way of calculating "almost equality":

    >>> np.testing.assert_allclose(expected, actual, rtol=0, atol=1e-3)
    Not equal to tolerance rtol=0, atol=0.001
    >>> np.testing.assert_allclose(expected, actual, rtol=0, atol=1e-2)

For more on the issues of testing and floating point numbers, see [Software Carpentry](http://software-carpentry.org/)'s [Testing: Floating Point](http://software-carpentry.org/v4/test/float.html) lesson.

So, with this in mind, could change our comparison in test_counts.py from:

    np.testing.assert_equal(expected, actual, \
      "freqs2013.dat not equal to testoracle/freqs2013.dat")

to:

    np.testing.assert_almost_equal(expected, actual, 2, 
      "freqs2013.dat not equal to testoracle/freqs2013.dat")

This helps to ensure that our tests will not suddenly fail if any refactorings result in subtle changes in floating point values within output files.

What is a suitable threshold for equality? That depends upon the doman, and the research being undertaken. For some fields, rounding to the nearest whole number may be acceptable. For others, far greater precision may be required.

## Add more tests

We now have a system, or end-to-end, test. Ideally, we'd want to add some (a lot!) moretests. For example, to test count_frequency with a minimum token length:

    result = os.system("count_frequency samples/events2013.dat freqs2013_5.dat 5")
    assert_equal(0, result, "Unexpected return code")
    assert_true(os.path.isfile("freqs2013_5.dat"), "Could not find freqs2013_5.dat")
    np.testing.assert_almost_equal(expected, actual, 2, 
      "freqs2013_5.dat not equal to testoracle/freqs2013_5.dat")

Another type of system test we can do is to check what happens when our software is not given valid inputs. For example, if we do not provide an output file name to count_frequency then a non-zero return code is expected:

    from nose.tools import assert_not_equal

    result = os.system("count_frequency samples/events2013.dat")
    assert_not_equal(0, result, "Unexpected return code")

## Clean up the test code

Up to now our test code is just a sequence of commands. We can exploit language-specific features to modularise our code. So, in Python we can split up our code into test functions e.g.

    def test_count_frequency():

    def test_count_frequency_minimum_token_length():

    def test_count_frequency_missing_output_file_name():

Test frameworks have conventions which, if test code conforms to these conventions, allows the test code to access the full power of the test framework. For example, nose comes with a command-line tool, nosetests, which looks for functions prefixed by "test_", runs these test functions and reports on the results. [test_count_frequency.py](./tests/test_count_frequency.py) has a modularised set of test functions and can be run, using nosetests, as follows:

    nosetests test_count_frequency.py
    ..Usage: python count_frequency.py INPUT_FILE OUTPUT_FILE [MINIMUM_LENGTH]
    .
    ----------------------------------------------------------------------
    Ran 3 tests in 2.940s

    OK

nosetests prints a "." for each test function that runs and passes.

Many xUnit test frameworks provide these capabilities so long as tests are written in a certain way. For example, in FRUIT for Fortran one writes test subroutines e.g.

    subroutine test_count_frequency()

In JUnit for Java one defines test classes (e.g. FrequencyCountTest) and marks up test methods with annotations e.g.

    @Test
    public void testCountFrequency()

See our repository [Build and test examples](https://github.com/softwaresaved/build_and_test_examples) for examples of test code written for the test frameworks of various languages.

## Examples in other languages

As an example of how the same approach can be used with other language, two other examples are available. These expect a testoracle directory to have been created as we described earlier, and these implement the same tests as our Python example.

[test_count_frequency.sh](./test_count_frequency.sh) provides an example of automated tests written as a bash shell script. It provides examples of running software, checking the return code, checking for output files, and comparing output files to those of the test oracle (though only a naive comparison using the diff command is adopted). 

If you have Linux/Unix then you can run this as follows:

    ./test_count_frequency.sh

[test_count_frequency.R](./test_count_frequency.R) provides an example of automated tests written as a bash shell script. It provides examples of running software, checking the return code, checking for output files, and comparing output files to those of the test oracle. It uses the [testthat](http://cran.r-project.org/web/packages/testthat/index.html) test framework for R.

If you have R and have installed the testthat library, then you can run this on Windows as follows:
 
    C:\Programs\R\R-3.1.0\bin\Rscript.exe testthat.R

You can run this on Linux/Unix as follows:

    Rscript testthat.R

## Conclusion

Automated testing can give researchers the security to refactor, extend, optimise or tidy, their code. The approach presented in this guide suggests a way that researchers can introduce automated testing for their software without the overhead of having to implement dozens of unit tests at the outset. 

This approach is also useful for developers recruited onto research projects, who know how to design, develop, refactor and optimise software but may lack the domain knowledge required to validate that the outputs are scientifically correct. So long as a researcher has validated the outputs used to create the test oracle, the developer can refactor, optimise and tidy the software, with some confidence that they are not undermining its scientific validity.

For more on automated testing and research software please see:

* [Testing your software](http://software.ac.uk/resources/guides/testing-your-software) - our guide on testing research software.
* [How continuous integration can help you regularly test and release your software](http://software.ac.uk/how-continuous-integration-can-help-you-regularly-test-and-release-your-software) - our guide on continuous integration which allows automated tests to triggered by changes to source code held within a source code repository like Git.
* [Testing](http://software-carpentry.org/v4/test/index.html) - [Software Carpentry](http://software-carpentry.org)'s lessons on testing.

## Acknowledgements, copyright and licence

Copyright (c) 2014 The University of Edinburgh.

Code is licensed under the [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html) licence. The licence text is also in [LICENSE-2.0.txt](./LICENSE-2.0.txt).

Documents are licensed under the Creative Commons [Attribution-NonCommercial 2.5 UK: Scotland (CC BY-NC 2.5 SCOTLAND)](http://creativecommons.org/licenses/by-nc/2.5/scotland/).

This guide draws upon ideas from [Software Carpentry](http://software-carpentry.org) and materials developed by [The Software Sustainability Institute](http://www.software.ac.uk) and [ARCHER](http://www.archer.ac.uk).
