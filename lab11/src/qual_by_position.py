import sys


def read_fastq(filename):
    # 4줄씩 묶어 (이름, 서열, 품질) 튜플 리스트로 돌려준다
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records


def qual_by_position(reads):
    # 위치(0부터)마다 품질 점수 합과 그 위치까지 온 read 수를 센다
    # read 길이가 제각각(trim 후)이어도 위치별 read 수로 나누므로 맞게 계산된다
    sums = []
    counts = []
    for name, seq, qual in reads:
        for i, ch in enumerate(qual):
            if i == len(sums):
                sums.append(0)
                counts.append(0)
            sums[i] = sums[i] + (ord(ch) - 33)   # Phred+33
            counts[i] = counts[i] + 1
    means = []
    for i in range(len(sums)):
        means.append(sums[i] / counts[i])
    return means, counts


def test():
    # 손으로 계산할 수 있는 작은 예로 확인한다
    # '!'=0, '+'=10, '5'=20, '?'=30, 'I'=40
    reads = [("r1", "ACG", "I?5"), ("r2", "AC", "5+")]
    means, counts = qual_by_position(reads)
    assert means == [30.0, 20.0, 20.0], means
    assert counts == [2, 2, 1], counts


test()

if len(sys.argv) < 2:
    print("사용법: python3 src/qual_by_position.py <FASTQ 파일> [출력 TSV]")
    sys.exit(1)

reads = read_fastq(sys.argv[1])
means, counts = qual_by_position(reads)

# 출력 파일을 주면 TSV로 저장하고, 없으면 화면에 출력한다
if len(sys.argv) >= 3:
    out = open(sys.argv[2], "w")
else:
    out = sys.stdout

out.write("position\treads\tmean_qual\n")
for i in range(len(means)):
    out.write(f"{i + 1}\t{counts[i]}\t{means[i]:.2f}\n")

if out is not sys.stdout:
    out.close()
    print("read 개수:", len(reads))
    print("최대 길이:", len(means))
    print("저장:", sys.argv[2])
