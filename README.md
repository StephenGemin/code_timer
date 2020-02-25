# code_timer

Simple python timer to use for single lines of code, or entire functions/classes


# New Features!

  - codetimer logger allowing you to set the streaming level or hide the logging entirely
  - Ability to use `code_timer.Timer` as a class, context manager, decorator
  - Ability to use separate `code_timer.timer` decorator


## Basic Usage

You can use `code_timer.Timer` in several different ways:

1. As a **class**:

    ```python
    t = Timer(name="class")
    t.start()
    # Do something
    t.stop()
    ```

2. As a **context manager**:

    ```python
    with Timer(name="context manager"):
        # Do something
    ```

3. As a **decorator**:

    ```python
    @Timer(name="decorator")
    def stuff():
        # Do something
    ```
    
You can also use the function defined decorator `code_timer.timer` instead of using the class decorator.  You can use it with or without the braces.
1.  ```python
    @timer
    def your_func():
        # Do something
    ```
2. ```python 
   @timer(name="my_timer")
   def your_func():
       # Do something
   ```