import sys 
  
STOPS = ["TAA", "TAG", "TGA"] 
  
def find_orfs(seq, frame): 
    orfs = [] 
    start = None 
  
    for i in range(frame, len(seq) - 2, 3): 
        codon = seq[i:i + 3] 
  
        if codon == "ATG" and start is None: 
            start = i 
        elif codon in STOPS and start is not None: 
            orfs.append((start, i + 3)) 
            start = None 

    return orfs 

# 역상보 서열을 만든다 (뒤집은 뒤 A<->T, G<->C 로 바꾼다)
def reverse_complement(seq): 
    pairs = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"} 
    return "".join(pairs.get(base, "N") for base in reversed(seq)) 
  
seq = sys.argv[1].upper() 
rc = reverse_complement(seq) 
  
for frame in [0, 1, 2]: 
    orfs = find_orfs(seq, frame) 
    print("틀", frame + 1, ":", orfs) 
    for s, e in orfs: 
        print("   ", seq[s:e], "길이", e - s) 

# 역상보 서열의 세 틀(-1, -2, -3)도 검사한다
# 위치는 역상보 서열 기준이다
for frame in [0, 1, 2]: 
    orfs = find_orfs(rc, frame) 
    print("틀", -(frame + 1), ":", orfs) 
    for s, e in orfs: 
        print("   ", rc[s:e], "길이", e - s) 