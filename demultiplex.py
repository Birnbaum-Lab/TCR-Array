
'''
This is Garrett code for separating TCRs by barcode for his 1/26/2017
Now compatible with Python 2.7 and Python 3.4
'''

# standard libraries
from __future__ import print_function
import os

# nonstandard libraries


# main code test block
def main():

    print('Starting main...')

    sorter = SequenceSorter()
    sorter.load_data('TCRs.fasta')
    sorter.start()
    sorter.publish_data()

    print('Finished main.')

'''
This class in generally designed for sequence analysis for TCR alpha and beta sequences
'''

class SequenceSorter:
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

        self.sequences = [[[[] for c in self.column_ids] for b in self.row_ids] for a in self.plate_ids]
        self.qualities = [[[[] for c in self.column_ids] for b in self.row_ids] for a in self.plate_ids]

    # load fasta/fastq data
    def load_data(self,fname=None):
        if not fname:
            print('No filename specified, data not loaded!')
            return False
        if not os.path.exists(fname):
            print('File not in directory, data not loaded!')
            return False
        if not fname.endswith('.fasta') and not fname.endswith('.fastq'):
            print('Currently only accepting .fasta and .fastq files!')
            return False
        else:
            print('Data selected successfully!')
            self.fname = fname
            if fname.endswith('.fasta'): # fasta parsing settings
                self.perline,self.seqshift,self.qualshift = 2,1,None
            if fname.endswith('.fastq'): # fastq parsing settings
                self.perline,self.seqshift,self.qualshift = 4,1,3     
            return True
                
    # start main program execution and identification
    def start(self):
        print('Starting sequence sorting...')
        with open(self.fname,'r') as myfile:
            print('File read.')
            lines = myfile.readlines()
            print('File loaded.')
            for i,line in enumerate(lines):
                if i%1000000 == 0 and i != 0: print('{} lines processed...'.format(i))
                if i%self.perline == self.seqshift:
                    var = len(line)
                    if sum([1 for id in self.plate_ids if line[2:7] == id]) == 1:
                        if sum([1 for id in self.row_ids if line[9:14] == id]) == 1:
                            if sum([1 for id in self.column_ids if line[(var-8):(var-3)] == id]) == 1:
                                if self.qualshift: # if this is a file format with quality scores 
                                    self.count_sequence(line,lines[i+2])            
                                else: # otherwise, we will just get a filler quality score (~ = 100% quality)
                                    self.count_sequence(line)
        print('Finished sorting!')

    # this quick function adds sequence to appropriate bin 
    def count_sequence(self,line,qual=None):
        var = len(line)
        a = [i for i,id in enumerate(self.plate_ids) if line[2:7] == id][0]
        b = [i for i,id in enumerate(self.row_ids) if line[9:14] == id][0]
        c = [i for i,id in enumerate(self.column_ids) if line[(var-8):(var-3)] == id][0] 
        self.plate_counts[a] += 1       
        self.row_counts[b] += 1       
        self.column_counts[c] += 1       
        self.sequences[a][b][c].append(line)
        if qual:
            self.qualities[a][b][c].append(qual)
        else:
            try: self.qualities[a][b][c].append('~'*len(line))
            except MemoryError:
                print('Memory error, maybe try running in 64-bit Python 2.7 or switching to Python 3.4')
                return False 

    # create a bunch of text files
    def publish_data(self,mode='group',silent=True,threshold=90):
        if not silent: print('Publishing data...')
            
        # separate each well into different text file
        if mode == 'separate':
            # if directory 'data' is not there...
            if not os.path.exists('./data'):
                os.makedirs('./data')
            for p_id,d3 in zip(self.plate_labels,self.sequences):
                for r_id,d2 in zip(self.row_labels,d3):
                    for c_id,d1 in zip(self.column_labels,d2):
                        print('{}{}{} has {} sequences.'.format(p_id,r_id,c_id,len(d1)))
                        with open('./data/{}{}{}.txt'.format(p_id,r_id,c_id),'w') as myfile:
                            for seq in d1:
                                if len(seq) > threshold:
                                    myfile.write(seq)

        # put identifiers to label each well in one text file
        elif mode == 'group':
            # write a bunch of txt files
            with open('seq_formatted.fastq','w') as myfile:
                for p_id,d3,d3q in zip(self.plate_labels,self.sequences,self.qualities):
                    for r_id,d2,d2q in zip(self.row_labels,d3,d3q):
                        for c_id,d1,d1q in zip(self.column_labels,d2,d2q):
                            if not silent: print('{}{}{} has {} sequences.'.format(p_id,r_id,c_id,len(d1)))
                            for seq,quality in zip(d1,d1q):
                                if self.anchor5 in seq and self.anchor3_alpha in seq: # check if alpha
                                    entry = seq[seq.index(self.anchor5):seq.index(self.anchor3_alpha)+len(self.anchor3_alpha)].replace('\n','') + '\n'
                                    qual = quality[seq.index(self.anchor5):seq.index(self.anchor3_alpha)+len(self.anchor3_alpha)].replace('\n','') + '\n'
                                    if len(entry) > threshold:
                                        myfile.write('@miseq_alpha\n')
                                        myfile.write('{}{}{}'.format(p_id,r_id,c_id) + 'AA' + entry)
                                        myfile.write('+\n')
                                        myfile.write('~'*(len('{}{}{}' .format(p_id,r_id,c_id))+2) + qual + '\n')
                                elif self.anchor5 in seq and self.anchor3_beta in seq: # check if beta
                                    entry = seq[seq.index(self.anchor5):seq.index(self.anchor3_beta)+len(self.anchor3_beta)].replace('\n','') + '\n'
                                    qual = quality[seq.index(self.anchor5):seq.index(self.anchor3_beta)+len(self.anchor3_beta)].replace('\n','') + '\n'
                                    if len(entry) > threshold:
                                        myfile.write('@miseq_beta \n')
                                        myfile.write('{}{}{}'.format(p_id,r_id,c_id) + 'GG' + entry) 
                                        myfile.write('+\n')
                                        myfile.write('~'*(len('{}{}{}' .format(p_id,r_id,c_id))+2) + qual + '\n')

        if not silent: print('Finished publishing!')

# catch for namespace
if __name__ == '__main__':
    main()












