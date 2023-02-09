<h1 align="center">IDoCT Format Checker</h1>

<p align="center">A format checking tool to ensure that changes made to files of the dataset do not violate any of the required rules.</p>

## Run Locally

#### 1. Check your Python version

This tool is recommended to be run using Python 3.9, however Python 3.7 and above should also work. You can check your Python version by typing `python -V` on your command line. For example:

```
$ python -V
Python 3.9.4
```

If doing that tells you you're working with Python 2.7, you should try `python3 -V`. If it's version 3.7 or above, you can run the tool following step number 3. Otherwise, you should consider installing the [latest Python version](https://www.python.org/downloads/).

#### 2. Install dependencies

The dependencies for this tool can be installed running the following from the root directory:

```
$ pip install requirements.txt
```

#### 3. Run the tool

Running this tool locally only requires running `main.py` from the root directory:

```
$ python main.py $ctest_matadata path$ $begin_line$ $end_line$
```
In case your Python version is 2.7 but your your Python3 version is 3.7 or above (see step 1), you should run it using `python3` instead of `python`. 
