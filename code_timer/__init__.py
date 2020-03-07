"""
The code for this project is entirely based on a lesson from RealPython.

Lesson link:
https://realpython.com/python-timer/#a-python-timer-context-manager

Repo link:
https://github.com/realpython/codetiming

This is a practice attempt to re-create the code and to upload a project to
PyPi.

I had a lot of trouble, and ultimately could not figure out, how to call
the class decorator without the braces (Ex. @Timer).  Maybe I'll figure it
out one day.  This was the reason I added the function decorator 'timer'

There are some differences from the RealPython Lesson:
  * I've added a functional decorator.  You have the ability to just use
    @timer whereas the class decorator requires @Timer()
  * code is based on Python 3.7 and does not use data classes
  * I've forced the use of logging, with the name 'code_timer'
  * I don't think print statements should have any place within production code
  * The log lines are hard coded, rather than being able to pass what you
    want when initializing the Timer class
  * I've added the __call__ instead of inheriting from ContextDecorator


1. As a **class**:
    t = Timer(name="class")
    t.start()
    # Do your thing(s) here
    t.stop()

2. As a **context manager**:
    with Timer(name="context manager"):
        # Do your thing(s) here

3. As a **decorator**, choose one of the following options:
    @Timer(name="decorator")
    @Timer()
    @timer
    @timer()
    @timer(name="decorator")
    def stuff():
        # Do your thing(s) here
"""
