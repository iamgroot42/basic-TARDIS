# Description of columns and values in the database available at http://nist.gov/pml/data/comp-notes.cfm#notes
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
import json

JSON_FILENAME = "periodic_table.json"
Base = declarative_base()
engine = create_engine('sqlite:///basic-TARDIS.db')


class AtomicTable(Base):
    __tablename__ = 'AtomicTable'

    index = Column(Integer, primary_key=True)
    mass_number = Column("Mass Number", Integer)
    atomic_number = Column("Atomic Number", Integer)
    symbol = Column("Symbol", String(5))
    isotopic_composition =  Column("Isotopic Composition", String(50))
    relative_atomic_mass =  Column("Relative Atomic Mass", String(50))
    standard_atomic_weight =  Column("Standard Atomic Weight", String(50))
    notes =  Column("Notes", String(50))

# Setting up metadata
Base.metadata.create_all(engine)


def one_time_populate():
	'''
	Function that reads the .json file containing data, and converts into an SQL database.
	Column headers of the database are same as that in the original dataset.
	'''
	# New session for populating the database
	Session = sessionmaker(bind = engine)
	session = Session()
	try:
		f = open(JSON_FILENAME, 'r')
		data = json.load(f)
	except:
		print "I/O error"
	ind = 1
	try:
		for i in range(len(data)):
		# Iterate over each isotope
			for j in range(len(data[i]['Data'])):
				# Iterate over each element
				row = data[i]['Data'][j]
				# Tuple representing element:
				element = AtomicTable(mass_number = row['Isotope'], atomic_number = data[i]['Atomic Number'],
					symbol = row['Symbol'], isotopic_composition = row['Isotopic Composition'],
					relative_atomic_mass = row['Relative Atomic Mass'], index = ind,
					standard_atomic_weight = row['Standard Atomic Weight'], notes = row['Notes'])
				# Unique index per element (isotope)
				ind += 1
				session.add(element)
		session.commit()
		return True
	except:
		print "DB related error (maybe DB exists already)"
		return False
