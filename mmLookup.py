# MaxMind GeoLite2 Geo-IP Lookup Tool
# 
# Checks if an ipaddress's exchange-provided country code matches
# the country Maxmind thinks the ipaddress is from
#
# To run this program:
# - download most recent copy of mmdb: http://dev.maxmind.com/geoip/geoip2/downloadable/ 
# - prepare a csv file of ipaddress-country code pairs
# - call mmdbLookup.py and pass csv file as command line argument. Example:
# python mmdbLookup.py inputCSV.csv /full/path/to/mmdb/GeoLite2-Country.mmdb
#
# ouputs a csv file where last column of each row displays TRUE if countries 
# match or didn't find the country in mmdb, or FALSE if they countries don't match
# 
# assumes that csv is in same dir as this script

import geoip2.database
import sys
import os.path
import csv

if len(sys.argv) < 3:
	print "Usage: python mmdbLookup.py inputCSV.csv /full/path/to/mmdb/GeoLite2-Country.mmdb"
	sys.exit()

# create the reader object that will read records from the maxmind database
# get path to mmdb from command-line arg, exit if mmdb not found
mmdb = sys.argv[2]
if(os.path.isfile(mmdb) == False):
	print "Can't find mmdb database, exiting"
	print "You can download the most recent copy of maxmine geolite db here: http://dev.maxmind.com/geoip/geoip2/downloadable/"
	sys.exit()
readerDB = geoip2.database.Reader(str(mmdb))

# open the file + its csv reader
# take location of csv file as command line argument
inputCSV = open(str(sys.argv[1]),'rU')
readerCSV = csv.reader(inputCSV, dialect=csv.excel)

# create output csv file + its csv writer
outputCSV = open(str(sys.argv[1])[:-4] + '_output.csv', 'w')
writerCSV = csv.writer(outputCSV, dialect=csv.excel)

print 'Running...'

# iterate over records in input csv
for row in readerCSV:
	# get ip, country from csv
	ip = row[0]
	dxCountry = row[1]
	# if mmdb ip address lookup succeeds, get the country
	try:
		mmdbCountry = readerDB.country(ip).country.iso_code # call mmdb with ip from csv
	except geoip2.errors.AddressNotFoundError:
		mmdbCountry = 'NIL'
	# if ip address lookup returned null, set to NIL
	if mmdbCountry is None:
		mmdbCountry = 'NIL'
	# if countries dont match and lookup was successful, flag it
	match = 'True'
	if (dxCountry != mmdbCountry and not (mmdbCountry == 'NIL')):
		match = 'False'
	# write output row into output csv
	writerCSV.writerow([ip, dxCountry, mmdbCountry, match])

inputCSV.close()
outputCSV.close()

print 'Done'
