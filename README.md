![build status](https://travis-ci.com/AvivHaliva/Brain-Overflow.svg?branch=master)
![codecov](https://codecov.io/gh/AvivHaliva/Brain-Overflow/branch/master/graph/badge.svg)
# brain_overflow
A system that supports a Brain Computer Interface — imaginary hardware (for now...) that can read minds, and upload snapshots of cognitions.


# Installation
1. Clone the repository and enter it:
```shell
$ git clone git@github.com:avivhaliva/brain_overflow.git
...
$ cd brain_overflow/
```

2. Run the installation script and activate the virtual environment:
```shell
$ ./scripts/install.sh
...
$ source .env/bin/activate
[brain_overflow] $ # you're good to go!
```
    
3. To check that everything is working as expected, run the tests:
```shell
$ pytest tests/
...
```

# Usage
### Client
The client streams congnition snapshots to the server from a sample that includes user information and multiple snapshots.
The sample uploading is based on the following arguments:
* path - the sample's path.
* file_format - the sample format: 'binary', 'protobuf', etc. default is 'protobuf'.
    Note that at the moment only protobuf and binary formats are supported.
* host - server ip. default is '127.0.0.1'.
* port - server port. default is 8000.

The client expose the following:
1. *CLI*
```
    $ python -m brain_overflow.client upload-sample \
        -h/--host '127.0.0.1'             \
        -p/--port 8000                    \
        'snapshot.mind.gz'
```
Note that host and port flags are optional.

2. *API*
```python
    >>> from brain_overflow.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz') 
```
