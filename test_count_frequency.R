# Copyright 2014-2015, The University of Edinburgh
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
# To run outwith R:
#   C:\Program Files\R\R-3.1.0\bin\Rscript.exe test_count_frequency.R
# To run within R:
#   source("test_count_frequency.R")
#
# These tests expect:
# - count_frequency to be in the path or the current directory.
# - Input files to be in a samples/ directory:
#   - events2013.dat
# - Test oracle files to be in a testoracle/ directory:
#   - freqs_events2013.dat created via 
#     count_frequency samples/events2013.dat testoracle/freqs_events2013.dat
#   - freqs5_events2013.dat created via 
#     count_frequency samples/events2013.dat testoracle/freqs_events2013.dat 5

library(testthat)

test.tolerance <- 1e-2

context("count_frequency tests")

test_that("Test count_frequency", {
  result <- system2("count_frequency", "samples/events2013.dat freqs_events2013.dat")
  expect_equal(0, result, info="Unexpected return code")
  expect_true(file.exists("freqs_events2013.dat"), info="Could not find freqs_events2013.dat")
  expected <- read.table("testoracle/freqs_events2013.dat", stringsAsFactors=FALSE, 
                         colClasses=("numeric"))
  actual <- read.table("freqs_events2013.dat", stringsAsFactors=FALSE, 
                       colClasses=("numeric"))
  expect_equivalent(dim(expected), dim(actual),
    info="Dimensions of freqs_events2013.dat not equal to testoracle/freqs_events2013.dat")
  expect_equal(expected, actual, tolerance=test.tolerance,
    info="freqs_events2013.dat not equal to testoracle/freqs_events2013.dat")
})

test_that("Test count_frequency with a minimum token length", {
  result <- system2("count_frequency", "samples/events2013.dat freqs5_events2013.dat 5")
  expect_equal(0, result, info="Unexpected return code")
  expect_true(file.exists("freqs5_events2013.dat"), info="Could not find freqs5_events2013.dat")
  expected <- read.table("testoracle/freqs5_events2013.dat", stringsAsFactors=FALSE, 
                         colClasses=("numeric"))
  actual <- read.table("freqs5_events2013.dat", stringsAsFactors=FALSE, 
                       colClasses=("numeric"))
  expect_equivalent(dim(expected), dim(actual),
    info="Dimensions of freqs5_events2013.dat not equal to testoracle/freqs5_events2013.dat")
  expect_equal(expected, actual, tolerance=test.tolerance,
    info="freqs5_events2013.dat not equal to testoracle/freqs5_events2013.dat")
})

test_that("Test count_frequency with a missing output file name", {  
  result <- system2("count_frequency", "samples/events2013.dat")
  expect_false(0 == result, info="Unexpected return code")
})
