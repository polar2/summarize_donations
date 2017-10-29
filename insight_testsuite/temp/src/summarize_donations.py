# import useful libraries
import os
import sys
from operator import itemgetter
from numpy import median

def main():
	# ensure command line call has correct number of parameters
	if len(sys.argv)!=4:
		print("You did not specify input and output files in the appropriate way. For further help, please see README file.")
		return 0
	# prepare (blank) dictionaries to store the contributions by zipcode and date, open first output file
	contrib_by_zip = {}
	contrib_by_date = {}
	open_output_file1 = open(sys.argv[2],"w")
	# open file, read a line from file, split file into variables
	with open(sys.argv[1]) as fp:
		for line in fp:
			new_line = line.rstrip("\n").split('|')
			if (len(new_line)!=21):
				print("The current line in the input data file does not match the expected input data format.")
				continue
			# ensure `CMTE_ID` and `TRANSACTION_AMT` fields are present and valid
			if (len(new_line[0])==9):
				CMTE_ID = new_line[0]
			else:
				print("CMTE_ID is invalid.")
				continue
			try:
				TRANSACTION_AMT = float(new_line[14])
			except ValueError:
				print("TRANSACTION_AMT is missing.")
				continue
			# ensure `OTHER_ID` is set to empty
			if (len(new_line[15])!=0):
				print("OTHER_ID is not empty.")
				continue
			# reformat the `ZIP_CODE`
			ZIP_CODE = new_line[10][0:5]
			# is `ZIP_CODE` a valid zipcode?
			if (len(ZIP_CODE)==5):
				# has there been a contribution to this `CMTE_ID` from this `ZIP_CODE` yet?
				if ZIP_CODE in contrib_by_zip:
					if CMTE_ID in contrib_by_zip[ZIP_CODE]:
						# if so, add to list and report running median, number of contributions, amount of contributions
						contrib_by_zip[ZIP_CODE][CMTE_ID].append(TRANSACTION_AMT)
						running_median = int(round(median(contrib_by_zip[ZIP_CODE][CMTE_ID])))
						num_contrib = len(contrib_by_zip[ZIP_CODE][CMTE_ID])
						sum_contrib = int(round(sum(contrib_by_zip[ZIP_CODE][CMTE_ID])))
						open_output_file1.write(CMTE_ID+"|"+ZIP_CODE+'|'+str(running_median)+'|'+str(num_contrib)+'|'+str(sum_contrib)+'\n')
					# if not, save and report contribution
					else:
						contrib_by_zip[ZIP_CODE][CMTE_ID] = [TRANSACTION_AMT]
						open_output_file1.write(CMTE_ID+"|"+ZIP_CODE+'|'+str(int(round(TRANSACTION_AMT)))+'|1|'+str(int(round(TRANSACTION_AMT)))+'\n')
				else:
					contrib_by_zip[ZIP_CODE] = {}
					contrib_by_zip[ZIP_CODE][CMTE_ID] = [TRANSACTION_AMT]
					open_output_file1.write(CMTE_ID+"|"+ZIP_CODE+'|'+str(int(round(TRANSACTION_AMT)))+'|1|'+str(int(round(TRANSACTION_AMT)))+'\n')
			# is `TRANSACTION_DT` a valid date?
			TRANSACTION_DT = new_line[13]
			try:
				TS_YEAR = int(TRANSACTION_DT[4:8])
				TS_MONTH = int(TRANSACTION_DT[0:2])
				TS_DAY = int(TRANSACTION_DT[2:4])
			except ValueError:
				continue
			if (TS_YEAR<1) or (TS_YEAR>3000):
				continue
			if (TS_MONTH<1) or (TS_MONTH>12):
				continue
			if (TS_DAY<1) or (TS_DAY>31):
				continue
			# has there been a contribution to this `CMTE_ID` on this `TRANSACTION_DT` yet?
			if TRANSACTION_DT in contrib_by_date:
				if CMTE_ID in contrib_by_date[TRANSACTION_DT]:
					# if so, add to list
					contrib_by_date[TRANSACTION_DT][CMTE_ID].append(TRANSACTION_AMT)
				# if not, save contribution
				else:
					contrib_by_date[TRANSACTION_DT][CMTE_ID] = [TRANSACTION_AMT]
			else:
				contrib_by_date[TRANSACTION_DT] = {}
				contrib_by_date[TRANSACTION_DT][CMTE_ID] = [TRANSACTION_AMT]
	# close input and first output files. delete zip code results
	fp.close()
	open_output_file1.close()
	del contrib_by_zip
	# calculate median, number of contributions, and amount of contributions by date
	reformed_results = []
	for a_date in contrib_by_date:
		for a_cmte in contrib_by_date[a_date]:
			median_contrib = int(round(median(contrib_by_date[a_date][a_cmte])))
			num_contrib = len(contrib_by_date[a_date][a_cmte])
			sum_contrib = int(round(sum(contrib_by_date[a_date][a_cmte])))
			reformed_date = a_date[4:8]+a_date[0:2]+a_date[2:4]
			reformed_results.append([a_cmte,a_date,median_contrib,num_contrib,sum_contrib,reformed_date])
	del contrib_by_date
	# sort results
	sorted_results = sorted(reformed_results,key=itemgetter(0,5))
	del reformed_results
	# report results by date
	open_output_file2 = open(sys.argv[3],"w")
	for a_row in sorted_results:
		open_output_file2.write(a_row[0]+"|"+a_row[1]+'|'+str(a_row[2])+'|'+str(a_row[3])+'|'+str(a_row[4])+'\n')
	open_output_file2.close()

if __name__ == "__main__":
	main()