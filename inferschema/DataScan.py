import pandas
import datetime
import os
from dateutil.parser import parse

def check_date(value, icount):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(value, fuzzy=False)
        return icount + 1
    except ValueError:
        return icount

def check_integer(value, icount):

    try:
        int(value)
        return icount + 1
    except ValueError:
        return icount

def check_float(value, icount):
    try:
        float(value)
        if value.count('.') == 1:
            return icount + 1
        else:
            return icount
    except ValueError:
        return icount

def run(valid_csv, sample_size, conf_factor):
	
	schema_dict = {}
	schema_list = []
	list_index = 0
	missing_values_list = ['']

	conf_threshold = round(sample_size * conf_factor)

	with open(valid_csv) as inputcsvfile:
		df = pandas.read_csv(valid_csv, delimiter=',', nrows=1)

	for col in df.columns:

		schema_list.append("")

		with open(valid_csv) as inputcsvfile:

			chunk = pandas.read_csv(inputcsvfile, delimiter=',', nrows=sample_size)

			if len(chunk.index) < sample_size:
				conf_threshold = round(len(chunk.index) * conf_factor)

			integerCount = 0
			floatCount = 0
			dateCount = 0

			for index, row in chunk.iterrows():

				integerCount = check_integer(str(row[col]), integerCount)

				if integerCount == conf_threshold:
					schema_list[list_index] = {'name': col, 'type': 'integer', 'format': 'default'}
					break

				floatCount = check_float(str(row[col]), floatCount)

				if floatCount == conf_threshold:
					schema_list[list_index] = {'name': col, 'type': 'number', 'format': 'default'}
					break

				dateCount = check_date(str(row[col]), dateCount)

				if dateCount == conf_threshold:
					schema_list[list_index] = {'name': col, 'type': 'datetime', 'format': 'default'}
					break						

		if schema_list[list_index] == "":
			schema_list[list_index] = {'name': col, 'type': 'string', 'format': 'default'}

		list_index += 1

	schema_dict = {'fields': schema_list, 'missingValues': missing_values_list}

	return schema_dict