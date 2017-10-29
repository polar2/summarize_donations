# Overview
This repository includes code to aggregate and report campaign contributions by zip code and by date.  The code takes as input data from the Federal Elections Commission (FEC) that conforms to the FEC data dictionary (http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml).

There may be a large number of contributions.  The code reads in this data line-by-line from a data file, enabling it to be modified to work in a situation where data is sequentially streamed in.

One section of code identifies the running median, total dollar amount, and total number of contributions by recipient and zip code as the code works its way through a (potentially large) data file on campaign contributions.  

Another script identifies the median, total dollar amount, and total number of contributions by recipient and date.  The relevant calculations are, in this case, performed after all the data have been ingested.  There are no duplicate recipient and date pairs and the results represent medians across the entire data set and not running medians. The data are sorted, primarily alphabetically by recipient and secondarily chronologically by date.

# Code Usage and Dependencies
The code can be used via the run.sh shell script in the root directory of this repository.  The user can also call the source python script themselves from the command line.  The call would be similar to the command from the run.sh file.

python ./src/summarize_donations.py ./input/itcont.txt ./output/medianvals_by_zip.txt ./output/medianvals_by_date.txt

The call uses python to open the source python script (./src/summarize_donations.py) referencing the input FEC file on individual campaign contributions (./input/itcont.txt) and the output files summarizing contributions by zip code (./output/medianvals_by_zip.txt) and by date (./output/medianvals_by_date.txt).

The python script source code here depends on the following modules and libraries.

1. The os and sys standard modules for python
2. The operator module for python
3. The numpy library for pyhton
