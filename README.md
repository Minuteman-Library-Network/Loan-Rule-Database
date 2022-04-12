# Loan Rule Database
 Scripts and queries for working with a sqlite database containing Sierra loan rule data
 
 I created a SQLite database just using [db browser](https://sqlitebrowser.org/) which has an easy import csv to table feature.  

For the loan rule table in Sierra I simply exported it right from Sierra using the new export button and then imported it in db browser creating a table called loan_rule with a file I saved as loan_rules.db
 
For the determiner table 
 
I exported it the same way
Opened it in Notepad++ and changed the encoding from UTF-8-BOM to UTF-8
I also added a column name (id) to the first field that was blank by default
Then I ran [loan rule determiner parser.py](https://github.com/Minuteman-Library-Network/Loan-Rule-Database/blob/main/loan%20rule%20determiner%20parser.py) which does two things

it separate out any number ranges in the itype and ptype fields into the discrete numbers 

it uploads the resulting table into the database as a table called determiner
 
As a bonus I also imported the location_myuser and itype_property_myuser tables from SierraDNA into the database just to make translating those codes easier on myself within queries.

So that built most of the database, the one other thing I did after (which I could probably just build into the parser script in the future) was to run [this query](https://github.com/Minuteman-Library-Network/Loan-Rule-Database/blob/main/queries/determiner_expanded.sql) to take all the multi-value itype and ptype entries in the determiner table and break them out into their own rows, essentially making a linking table similar to something like bib_record_item_record_link in SierraDNA.  I then saved the results as a view in the database for use with future queries.

Then with all that you can start playing around with queries.  I've uploaded [a folder](https://github.com/Minuteman-Library-Network/Loan-Rule-Database/tree/main/queries) with a few I've played with for auditing rules just using the database itself.  And then for tying the information back into Sierra I have [an example Python script](https://github.com/Minuteman-Library-Network/Loan-Rule-Database/blob/main/on%20time%20returns%20by%20fine.ipynb) that links the daily fine rates from the loan_rule database with recent checkins from the circ_trans table.  This is my first attempt to try to compare activity at libraries that have gone fines free with those who have not.
