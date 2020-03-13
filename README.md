# code_timer
Simple python timer to use for single lines of code, or entire functions/classes

[![Latest version](https://img.shields.io/pypi/v/code_timer.svg)](https://pypi.org/project/code_timer/)
[![Python versions](https://img.shields.io/pypi/pyversions/code_timer.svg)](https://pypi.org/project/code_timer/)
[![CircleCI](https://circleci.com/gh/StephenGemin/code_timer.svg?style=shield)](https://app.circleci.com/pipelines/github/StephenGemin/code_timer)

# New Features!

  - Use `code_timer.Timer` as a class, context manager, decorator
    - Offers the most versatility and flexibility for your needs
  - Use separate `code_timer.timer` decorator
  - Use `code_timer.timeit` decorator to measure the time to run the same function multiple times
    - Useful when comparing the efficiency of one runtime vs another
    - By default, will run the function 10,000 times.  The number of runs is configurable
    - DO NOT USE THIS FOR RECURSIVE FUNCTIONS!!
  - Logger allowing you to set the streaming level or hide the logging entirely
  


## Basic Usage

#### `code_timer.Timer`

1. As a **class**: 

    ```python
    t = Timer(name="class")
    t.start()
    # Do something
    t.stop()
    ```

2. As a **context manager**:
  * Useful when trying to time a recursive function
  
    ```python
    with Timer(name="context manager") as t:
        # Do something
    print(f"Elapsed time: {t.elapsed_time}")
    ```

3. As a **decorator**:

    ```python
    @Timer(name="decorator")
    def stuff():
        # Do something
    ```
    
#### `code_timer.timer`

1. Without braces

    ```python
    @timer
    def your_func():
        # Do something
    ```
    
2. With braces
 
    ```python
    @timer(name="my_timer")
    def your_func():
        # Do something
    ```
    
#### `code_timer.timeit`
  - Time is reported at logging level: logging.INFO 
  - The following assumes the standard formatting for the code_timer logger

1. Default
    - will repeat the function 10,000 times and report the fastest three runs
  
    ```python
    @timeit
    def your_func():
        # Do something
    ```
    - Output: `2020-03-12 21:56:46: code_timer.INFO - Best 3 of 10000 for your_func: 0.2200 ms; 0.2220 ms; 0.2232 ms` 
    
2. Pass in the number of times to repeat
    ```python
    @timeit(num_repeats=50)
    def your_func():
        # Do something
    ```
    - Output: `2020-03-12 21:56:46: code_timer.INFO - Best 3 of 50 for your_func: 0.2200 ms; 0.2220 ms; 0.2232 ms` 
