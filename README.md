# tableausdk-python

Tableau SDK for Python. Currently this contains only the Document API. We are just getting started and this will evolve. Help us by submitting feedback, issues, and pull requests!

Document API
---------------
This is the supported way to programmatically change Tableau files such as .twb and .tds. If you've been doing "XML hacking" this is for you too :)

Check out the examples to see how to use it.

Currently only the following operations are supported:

* Modify database server
* Modify database name
* Modify database user

We don't yet support creating files from scratch. Support for .twbx and .tdsx is coming.

##### Getting Started
We will put this in PyPi to make installation easier. In the meantime, install the package locally with:
```python
pip install -e <directory containing setup.py>
```
