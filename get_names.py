import csv
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

with open('hmda_merged_Genesee_County.csv','r') as csvinput:
    reader = csv.reader(csvinput)
    id_names = {}
    names = []
    row = next(reader)
    for row in reader:
        rowid = row[2]
        name = row[87]
        if name not in names:
            names.append(name)
        if name not in id_names.keys():
            id_names[name] = rowid

id_names['DORT FCU'] = 7569
names.append('DORT FCU')
id_names['GMAC MTG'] = 23-1694840
names.append('GMAC MTG')
print ("done creating dict")
with open('zillow_merged_Genesee_County_census.csv', 'r') as csvinput:
    with open('zillow_merged_Genesee_County_filtered_census_names_90.csv', 'wb') as csvoutput:
        print ("started writing")
        writer = csv.writer(csvoutput)
        reader = csv.reader(csvinput)
        all = []
        row = next(reader)
        row.append('respondent_id')
        writer.writerow(row)
        for row in reader:
            name = row[11]
            if name == "":
                rid = " "
            else:
                if name in id_names.keys():
                    rid = id_names[name]
                else:
                    extracted = process.extractOne(name, names)
                    num = extracted[1]
                    match = extracted[0]
                    if num > 90 and match in id_names.keys():
                        rid = id_names[match]
                        id_names[name] = rid
                        names.append(name)
                    else:
                        rid = " "
                        id_names[name] = rid
                        names.append(name)
            row.append(rid)
            writer.writerow(row)
        print "done reading zillow"
#
print "done writing"
#