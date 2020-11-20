import pandas
import datetime
import os
import traceback
from dateutil.parser import parse
from datetime import time

def check_datetime(value):
    """
    Return whether the string can be interpreted as a date or datetime.

    :param string: str, string to check for date
    :param fuzzy: bool, to include natural language texts
    """
    try:
    	# cast the string value as date
    	dv = parse(value, fuzzy=False)
    	if dv.time().__str__() == "00:00:00":
    		return True, "date"
    	else:
    		return True, "datetime"
    except ValueError:
    	return False, "none"
    except:
    	#traceback.print_exc()
    	return False, "none"

def check_integer(value):

    try:
    	#cast the string value as INT
        int(value)
        return True
    except ValueError:
        return False
    except:
    	#traceback.print_exc()
    	return False

def check_float(value):
    try:
    	#cast the string value as float
        float(value)
        #Check if the decimal point exists
        if value.count('.') == 1:
            return True
        else:
            return False
    except ValueError:
        return False
    except:
    	#traceback.print_exc()
    	return False

def check_boolean(value):
	true_list = ["true", "t", "1", "on","y", "yes"]
	false_list = ["false", "f", "0", "off","n", "no"]
	
	try:
		if value.strip().lower() in true_list:
			return True
		elif value.strip().lower() in false_list:
			return True
		else:
			return False
	except:
		return False

def run(valid_csv, sample_size, conf_factor):
	
	schema_dict = {}
	schema_list = []
	list_index = 0
	missing_values_list = ['']

	conf_threshold = round(sample_size * conf_factor)

	try:
		with open(valid_csv) as inputcsvfile:
			df = pandas.read_csv(valid_csv, delimiter=',', nrows=1)

		for col in df.columns:

			# Initially for each column set the data type list to empty string
			schema_list.append("")
			inputcsvfile = None

			with open(valid_csv) as inputcsvfile:
				#data frame with the sample size
				dfs = pandas.read_csv(inputcsvfile, delimiter=',', nrows=sample_size)

				if len(dfs.index) < sample_size:
					conf_threshold = round(len(dfs.index) * conf_factor)

				integerCount = 0
				floatCount = 0
				booleanCount = 0
				dateCount = 0
				dateTimeCount = 0

				for index, row in dfs.iterrows():

					if check_integer(str(row[col])):
						integerCount += 1

						if integerCount == conf_threshold:
							schema_list[list_index] = {'name': col, 'type': 'integer', 'format': 'default'}
							break

					if check_float(str(row[col])):
						floatCount += 1

						if floatCount == conf_threshold:
							schema_list[list_index] = {'name': col, 'type': 'number', 'format': 'default'}
							break

					if check_boolean(str(row[col])):
						booleanCount += 1

						if booleanCount == conf_threshold:
							schema_list[list_index] = {'name': col, 'type': 'boolean', 'format': 'default'}
							break

					is_datetimevalue, datetime_type = check_datetime(str(row[col]))

					if is_datetimevalue and datetime_type == "date":
						dateCount += 1
						if dateCount == conf_threshold:
							schema_list[list_index] = {'name': col, 'type': 'date', 'format': 'default'}
							break

					elif is_datetimevalue and datetime_type == "datetime":
						dateTimeCount += 1
						if dateTimeCount == conf_threshold:
							schema_list[list_index] = {'name': col, 'type': 'datetime', 'format': 'default'}
							break

				del dfs

			# if no match in data type, by default set it to string
			if schema_list[list_index] == "":
				schema_list[list_index] = {'name': col, 'type': 'string', 'format': 'default'}

			list_index += 1

		del df
		schema_dict = {'fields': schema_list, 'missingValues': missing_values_list}

	except FileNotFoundError:
		schema_dict = {}
		print("File does  not exist!")		
	except:
		schema_dict = {}
		print("Error while processing the file!", traceback.print_exc())

	finally:
		return schema_dict