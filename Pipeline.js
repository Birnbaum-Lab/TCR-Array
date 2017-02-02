java -jar migec.jar Checkout -o -cute barcodes.txt seq_formatted.fastq.gz . ./checkout/
java -jar migec.jar Histogram checkout/ histogram/
java -jar migec.jar Assemble -M 128 -c checkout/S0_R0.fastq.gz . assembly/
java -jar migec.jar CdrBlast -a -S MusMusculus -R TRA,TRB assembly/S0_R0.t128.fastq.gz cdrblast/S0_asm.cdrblast.txt