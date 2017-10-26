#
# This shell script runs the python script in this repository: summarize_donations.py.
# It takes as input the specified input file: itcont.txt.
# It produces as output the specified output files: medianvals_by_zip.txt and medianvals_by_date.txt.
#
python ./src/summarize_donations.py ./input/itcont.txt ./output/medianvals_by_zip.txt ./output/medianvals_by_date.txt

