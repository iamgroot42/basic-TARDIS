# basic-TARDIS
Some scripts to download atomic elements' data, parse it and store it in a database. (Part of proposal for GSoC '16)

### How it works
* Data is downloaded from DATA_LINK (parses has been coded to match formatting of <a href = "http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=&all=all&ascii=html">this</a> website)
* Parses data using pyquery,beautifulsoup, writes it into a .json
* Another script reads this .json and creates an SQLAlchemy database

##Running the scripts
* ```pip install -r requirements``` to install dependencies
* ```python task_zero.py``` to generate the DB