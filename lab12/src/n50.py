import sys 
  
def read_fasta(filename): 
    seqs = {} 
    name = None 
    with open(filename) as f: 
        for line in f: 
            line = line.rstrip() 
            if line.startswith(">"): 
                name = line[1:].split()[0] 
                seqs[name] = "" 
            else: 
                seqs[name] = seqs[name] + line 
    return seqs 
  
def n50(lengths): 
    lengths = sorted(lengths, reverse=True) 
    total = sum(lengths) 
    half = total / 2 
  
    running = 0 
    for length in lengths: 
        running = running + length 
        if running >= half: 
            return length 
  
seqs = read_fasta(sys.argv[1]) 
lengths = [] 
for name in seqs: 
    lengths.append(len(seqs[name])) 
  
print("contig 개수:", len(lengths)) 
print("전체 길이:", sum(lengths)) 
print("가장 긴 contig:", max(lengths)) 
print("N50:", n50(lengths))

# 모든 contig 길이를 내림차순으로 정렬하여 한 줄에 하나씩 저장한다
# 출력 파일은 두 번째 인자로 바꿀 수 있다 (기본값: doc/contig_lengths.txt)
if len(sys.argv) > 2:
    outfile = sys.argv[2]
else:
    outfile = "doc/contig_lengths.txt"

with open(outfile, "w") as out:
    for length in sorted(lengths, reverse=True):
        out.write(str(length) + "\n")

print("contig 길이 저장:", outfile)