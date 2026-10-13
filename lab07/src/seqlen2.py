import sys
from fasta import read_fasta

seqs = read_fasta(sys.argv[1])
for name in seqs:
    print(len(seqs[name]))


##출력된 내용
#$ python3 seqlen2.py ../data/seqs.fasta
30
15
22