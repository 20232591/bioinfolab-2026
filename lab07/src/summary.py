import sys
from fasta import read_fasta, gc_content
 
infile = sys.argv[1]
outfile = sys.argv[2]
seqs = read_fasta(infile)
 
with open(outfile, "w") as out:
    out.write("name\tlength\tgc\n")
    for name in seqs:
        seq = seqs[name]
        gc = round(gc_content(seq), 4)
        out.write(name + "\t" + str(len(seq)) + "\t" + str(gc) + "\n")
 
print(len(seqs), "개 서열을", outfile, "에 저장했습니다.")

#@20232591 ➜ /workspaces/bioinfolab-2026/lab07 (main) $ python3 src/summary.py data/seqs.fasta doc/summary.tsv
#3 개 서열을 doc/summary.tsv 에 저장했습니다.
#@20232591 ➜ /workspaces/bioinfolab-2026/lab07 (main) $ cat doc/summary.tsv
#name    length  gc
#GENE1   34      0.4412
#GENE2   17      0.4118
#GENE3   24      0.5

#8번 
#$ wc -l doc/summary.tsv 출력결과 4 doc/summary.tsv
#$ cut -f1 doc/summary.tsv 