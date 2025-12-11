#!/bin/bash

# script to download data and process decay data and fission yield data

# download data from internet
mkdir -p rawData
curl -o ./rawData/endf-data.zip https://www.nndc.bnl.gov/endf-b8.0/zips/ENDF-B-VIII.0.zip

# unzip files
unzip ./rawData/endf-data.zip -d ./rawData

# run python scripts to create data in ./procData
mkdir -p procData
mkdir -p procData/FY
python ./dataSolver/decayPreProcessing.py
python ./dataSolver/FYpreprocessing.py

