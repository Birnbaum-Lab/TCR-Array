
'''
This is for formating data once concensus reads have been found and HiV regions have been identified
'''

# standard libraries
from __future__ import print_function
import os

# nonstandard libraries
import xlrd
import numpy as np
import matplotlib.pyplot as plt

# library configuration


# main function
def main():
    array = ArrayPublish()
    array.load_data('TCR_data.xlsx')
    array.start()

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
        self.plate_counts = [0 for i in range(len(self.plate_ids))]

        self.row_ids = ['TAAGC','TGCAC','CTCAG','GGAAT','CGAGG','AGGAG','TGTTG','CAACT']
        self.row_labels = ['TAAGC','TGCAC','CTCAG','GGAAT','CGAGG','AGGAG','TGTTG','CAACT']
        self.row_counts = [0 for i in range(len(self.row_ids))]

        self.column_ids = ['TGAAC','TCCTG','TATAA','ACAGG','GCGGT','TAAGT','CTAGC','ACGTC','TAGCC','CATTC','GTTGG','GTCTC']
        self.column_labels = ['TGAAC','TCCTG','TATAA','ACAGG','GCGGT','TAAGT','CTAGC','ACGTC','TAGCC','CATTC','GTTGG','GTCTC']
        self.column_counts = [0 for i in range(len(self.column_ids))] 

    def train(self,model=None):
        self.anchor5,self.anchor3_alpha,self.anchor3_beta = model.anchor5,model.anchor3_alpha,model.anchor3_beta
        self.plate_ids,self.plate_labels,self.plate_counts = model.plate_ids,model.plate_labels,model.plate_counts 
        self.row_ids,self.row_labels,self.row_counts = model.row_ids,model.row_labels,model.row_counts 
        self.column_ids,self.column_labels,self.column_counts = model.column_ids,model.column_labels,model.column_counts 

    def load_data(self,fname=None):
        if not fname:
            print('No filename specified, data not loaded!')
            return False
        if not os.path.exists(fname):
            print('File not in directory, data not loaded!')
            return False
        if not fname.endswith('.xlsx'):
            print('Currently only accepting .xlsx!')
            return False
        else:
            print('Data selected successfully!')
            self.fname = fname
            return True
       
    def start(self):
        wb = xlrd.open_workbook(self.fname)
        sheet = wb.sheet_by_name('Sheet1')
        headers = [str(cell.value) for cell in sheet.row(0)]
        print(headers)

    def publish(self,mode='test'):
        pass

# namespace catch
if __name__ == '__main__':
    main()

