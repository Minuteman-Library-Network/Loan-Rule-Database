"""
Use this python script to convert the loan rule determiner table from sierra
into an excel-style csv file to be used by other data processing tools
(sample file is included at the end of this script)
"""

import csv
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, delete

def is_num(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def expand_list(values_str):
    """
    Given a string of values (values_str): "1,2,3-5" for example, this function will return
    a list of the values expanded: list(1,2,3,4,5) from the above example
    """
    # create the return list
    item_type_list_expanded = list()

    # split the string to a list by the ',' character
    values_str_list = values_str.split(',')
    for num in values_str_list:
        if is_num(num):
            item_type_list_expanded.append(int(num))
        else:
            range_list = num.split('-')
            for i in range(int(range_list[0]), (int(range_list[1]) + 1)):
                item_type_list_expanded.append(i)
                # print(int(i))

    return(item_type_list_expanded)


"""
"data.txt" file should have a first line like this to define the columns:
location|patron_type|item_type|age_range|rule_number|active|unknown
"""
# our output file will be another csv file but ... better!
output_data = open('output_data.csv', 'w', newline='')
fieldnames = ('id', 'location', 'patron_type', 'item_type', 'age_range', 
    'rule_number', 'active', 'editable_by')

csv_writer = csv.DictWriter(output_data, fieldnames=fieldnames, 
    dialect='excel')

# write the field names to the new csv
csv_writer.writeheader()

#determiner_export.csv is a copy of the loan rule determiner table exported from Sierra with two changes
#in notepad++ I had to remove the BOM encoding and I had to provide a label for the first column, for the code below I chose to call it id

with open('determiner_export.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')

    print(csv_reader.fieldnames)
    for row in csv_reader:        
        # replace the row that had 'item_type' with the expanded version in a new dict (that will be mapped
        # in the )
        new_row = {
            'id': row['id'],
            'location': row['Location'],
            'patron_type': expand_list(row['Patron Type']),
            'item_type': expand_list(row['Item Type']),
            'age_range': row['Age Range'],
            'rule_number': row['Rule Number'],
            'active': row['Active'],
            'editable_by': row['Editable By']
        }
        # write this row ...
        csv_writer.writerow(new_row)

# close output file
output_data.close()
output_data = open('output_data.csv', 'r')

col_list = ["id","location","patron_type","item_type","rule_number","active","editable_by"]
df_determiner = pd.read_csv(output_data, usecols=col_list, dtype={"id":"int","location":"str","patron_type":"str","item_type":"str","rule_number":"int","active":"str","editable_by":"str"})   

output_data.close()

engine = create_engine("sqlite:///loan_rules.db")
df_determiner.to_sql('determiner', con=engine, index=False, if_exists='replace')

engine.dispose()
