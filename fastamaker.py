out =[]

with open('S0_R0.t128.fastq','r') as myfile:
	lines = myfile.readlines()
	for i,line in enumerate(lines):
		if i%4==1:
			var = lines[i-1]
			lenvar = len(lines[i-1])
			out.append('>'+var[1:lenvar])
			out.append(lines[i])

fastafile = open('TCRsfasta.fastq','w')

for i in out:
	fastafile.write("%s" % i)