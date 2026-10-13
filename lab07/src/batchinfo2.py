import sys
import glob
from fasta import read_fasta, gc_content

folder = sys.argv[1]
outfile = sys.argv[2]

with open(outfile, "w") as out:
    out.write("filename\tcount\ttotal\tmean_gc\n")
    for f in glob.glob(folder + "/*.fasta"):
        seqs = read_fasta(f)
        count = len(seqs)
        total = 0
        gc_sum = 0
        for name in seqs:
            total = total + len(seqs[name])
            gc_sum = gc_sum + gc_content(seqs[name])
        out.write(f + "\t" + str(count) + "\t" + str(total) + "\t" + str(round(gc_sum/count, 4)) + "\n")

print("저장 완료:", outfile)