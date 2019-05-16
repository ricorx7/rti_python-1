# rti_python
RTI Library in Python


Rowe Technologies Inc. Python library

There is currently no main file to run.  This library contains core library files to create a python application.


# Dependencies
Must use Python version 3.5

OSX and Linux
```javascript
pip3 install -r requirements.txt -UI --user
```
 
 
Windows
```javascript
python -m pip install -r requirements.txt -UI --user
```


### Upgrade Dependcies to Latest Version
```term
pip install -r requirements.txt --upgrade
```

## ADCP
All the available commands and subsystem types.  This also contains the prediction model

## Codecs
Decode the ADCP data from different formats.

## Ensemble
Ensemble data formats

## Unittest
All the unittests.


## Waves
Waves MATLAB formats

## Writer
Write the ensemble data to a file format.

## Logging
Edit the log.py file to turn on or off some logging options.

## Read in a File and decode the data
```python
from rti_python.ADCP.ReadBinaryFile import ReadBinaryFile


CHUNKSIZE = 1024
FILE_PATH = "/path/to/file/ensembleFile.bin"


def ens_handler(sender, ens):
    print("ens number %s" % ens.EnsembleData.EnsembleNumber)


reader = ReadBinaryFile()
reader.ensemble_event += ens_handler
reader.playback(FILE_PATH)
```