
'''
This the main file for execution in the workflow for TCR array analysis
Imports other main scripting files:
    (demultiplex.py)
    (arraypublish.py)
to achieve a consistent workflow
'''

from demultiplex import *
from arraypublish import *

print 'Starting main...'

sorter = SequenceSorter()
sorter.load_data('TCRs.fastq')
sorter.start()
sorter.publish_data()

print 'Finished main.'

