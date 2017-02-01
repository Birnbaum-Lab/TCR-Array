
'''
This is for formating data once concensus reads have been found and HiV regions have been identified
'''

# standard libraries
from __future__ import print_statement

# nonstandard libraries
from openpyxl import Workbook,load_workbook

# library configuration


# main function
def main():
    pass


'''
Class: ArrayPublish
Function:
    Generates some cute figures from the output of HiV...
'''
class ArrayPublish:
    # intialize program with appropriate barcodes (available for modification)
    def __init__(self):

        self.anchor5 = 'CCAGGGTTTTCCCAGTCACGAC' # variable region ID
        self.anchor3_alpha = 'GACTCCCAAATCAATGTGC' # alpha chain ID
        self.anchor3_beta = 'GGTCTCCTTGTTTGAGCCATC' # beta chain ID

        rows = list('ABCDEFGH')

        self.plate_ids = ['GCAGA','TCGAA','AACAA','GGTGC','TTGGT']
        self.plate_labels = ['GCAGA','TCGAA','AACAA','GGTGC','TTGGT']
        self.plate_counts = [0 for i in xrange(len(self.plate_ids))]

        self.row_ids = ['TAAGC','TGCAC','CTCAG','GGAAT','CGAGG','AGGAG','TGTTG','CAACT']
        self.row_labels = ['TAAGC','TGCAC','CTCAG','GGAAT','CGAGG','AGGAG','TGTTG','CAACT']
        self.row_counts = [0 for i in xrange(len(self.row_ids))]

        self.column_ids = ['TGAAC','TCCTG','TATAA','ACAGG','GCGGT','TAAGT','CTAGC','ACGTC','TAGCC','CATTC','GTTGG','GTCTC']
        self.column_labels = ['TGAAC','TCCTG','TATAA','ACAGG','GCGGT','TAAGT','CTAGC','ACGTC','TAGCC','CATTC','GTTGG','GTCTC']
        self.column_counts = [0 for i in xrange(len(self.column_ids))] 



# namespace catch
if __name__ == '__main__':
    main()

