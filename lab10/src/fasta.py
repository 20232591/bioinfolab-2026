"""FASTA 파일을 다루는 함수 모음"""

def read_fasta(filename): 
    """FASTA 파일을 읽어 {이름: 서열} 딕셔너리로 돌려준다.""" 
    seqs = {} 
    name = None 
    with open(filename) as f: 
        for line in f: 
            line = line.rstrip().upper()
            if line.startswith(">"): 
                name = line[1:].split()[0] 
                seqs[name] = "" 
            else: 
                seqs[name] = seqs[name] + line 
    return seqs 

def write_fasta(seqs, filename):
    """{이름: 서열} 딕셔너리를 FASTA 파일로 저장한다."""
    with open(filename, "w") as out:
        for name in seqs:
            out.write(">" + name + "\n")
            out.write(seqs[name] + "\n")

  
  
def gc_content(seq): 
    """서열의 GC 비율을 0과 1 사이의 수로 돌려준다.""" 
    if len(seq) == 0: 
        return 0.0 
    gc = seq.count("G") + seq.count("C") 
    return gc / len(seq) 


def reverse_complement(seq):
    """서열의 역상보 서열을 돌려준다."""
    table = {"A": "T", "T": "A", "G": "C", "C": "G"}
    comp = ""
    for base in seq:
        comp = comp + table[base]
    return comp[::-1]


def length_stats(seqs):
    """서열 딕셔너리의 길이 통계를 돌려준다."""
    lengths = [len(seq) for seq in seqs.values()]
    return {
        "count": len(lengths),
        "total": sum(lengths),
        "mean": round(sum(lengths) / len(lengths), 2),
        "min": min(lengths),
        "max": max(lengths)
    }


if __name__ == "__main__": 
    import sys 
    seqs = read_fasta(sys.argv[1]) 
    for name in seqs: 
        print(name, len(seqs[name]), round(gc_content(seqs[name]), 3))
    
    # 역상보 테스트
    seq = "ATGCGATACGCTTGA"
    assert reverse_complement(reverse_complement(seq)) == seq
    print("역상보 테스트 통과:", reverse_complement(seq))

#read_fasta 의 rstrip()을 upper()로 바꾸어 서열을 대문자로 출력되도록 했다.
#출력 결과 
    
#$ python3 src/fasta.py data/lower.fasta  $ python3 src/fasta.py data/lower.fasta
#LOW1 11 0.455
#LOW2 361 0.061
#역상보 테스트 통과: TCAAGCGTATCGCAT

#3.고친 뒤에 다시 실행
#fasta.py 실행시 LOW1 11 0.455 LOW2 361 0.061 역상보 테스트 통과: TCAAGCGTATCGCAT 3줄로 출력된다. 
#countseq2.py 실행시 2가 출력된다.
#seqlen2.py 실행시 11 361이 두 줄로 출력된다. 

#같은 수정을 06번 방식(스크립트마다 복사)로 했다면 몇 군데를 고쳐야했을까?
#파일마다 rstrip()이나 lower()을 upper()로 고치거나 ...
