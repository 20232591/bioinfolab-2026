import sys
from fasta import read_fasta, write_fasta
 
infile = sys.argv[1]
minlen = (sys.argv[2])
outfile = sys.argv[3]
 
seqs = read_fasta(infile)
 
selected = {}
for name in seqs:
    if len(seqs[name]) >= minlen:
        selected[name] = seqs[name]
 
write_fasta(selected, outfile)
print(len(seqs), "개 중", len(selected), "개를", outfile, "에 저장했습니다.")

#int(sys.argv[2])에서 int를 빼면 File "/workspaces/bioinfolab-2026/lab07/src/filter_fasta.py", line 12, in <module>
#if len(seqs[name]) >= minlen:
#TypeError: '>=' not supported between instances of 'int' and 'str'