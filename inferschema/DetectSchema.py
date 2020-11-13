#from tableschema import Table, infer, Schema
from tableschema import infer
import json
import argparse
import sys

def run(file_name, sample_size:int, conf_factor:float = 0.75, cloud_service = 'bigquery'):
	# This function returns a dictionary with column names as keys and data types as values

	dict_datatype_maps = {}

	if cloud_service.lower() == "bigquery":
		# Below dictionary is data type mappings from python to bigquery
		dict_datatype_maps = {
			"string": "STRING",
	  		"date": "DATE",
	  		"integer": "INT64",
	  		"object": "STRING",
	  		"datetime": "TIMESTAMP",
	  		"number": "FLOAT64",
	  		"boolean": "BOOL",
	  		"geopoint": "GEOGRAPHY",
	  		"array" : "ARRAY" 
		}
	else:
		return

	schema_dict = {}

	schema = infer(file_name, limit=sample_size, confidence=conf_factor)
	#The returned schema is of dictionary type with the below format
	#{'fields': [{'name': '<column name>', 'type': '<actual data type>', 'format': 'default'}], 'missingValues': ['']}

	# This has to be reformatted into a more user friendly dictionary format based on the target cloud service
	for k, v in schema.items():
		if k == 'fields':
			for x in v:
				for k1, v1 in x.items():
					if k1 == 'name':
						column_name = v1
					if k1 == 'type':
						data_type = dict_datatype_maps[v1]

				schema_dict[column_name] = data_type

	return schema_dict

def main(argv=None):
	
	parser = argparse.ArgumentParser()

	parser.add_argument('-fn', dest='file_name', required=True, help='File Name')
	parser.add_argument('-ss', type=int, dest='sample_size', required=True, help='sample size')
	parser.add_argument('-cf', type=float, dest='conf_factor', required=True, help='confidence factor between 0 and 1')
	parser.add_argument('-cs', dest='cloud_service', required=True, help='cloud service')
	
	args = parser.parse_args(argv)

	schema_dict = run(args.file_name, args.sample_size, args.conf_factor, args.cloud_service)

	print(schema_dict)

if __name__ == '__main__':
    sys.exit(main())