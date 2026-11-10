import os
import sys

# gc_content 함수는 lab07/src/fasta.py 에 있으므로 그 폴더를 import 경로에 추가한다
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lab07", "src"))
from fasta import gc_content


def read_fastq(filename):
    # 4줄씩 묶어 (이름, 서열, 품질) 튜플 리스트로 돌려준다
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip().upper()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records


def gc_summary(reads):
    # 전체 GC 비율(염기 기준)과 read별 GC 비율 리스트를 구한다
    total_gc = 0
    total_len = 0
    read_gc = []
    for name, seq, qual in reads:
        total_gc = total_gc + seq.count("G") + seq.count("C")
        total_len = total_len + len(seq)
        read_gc.append(gc_content(seq))
    overall = total_gc / total_len if total_len > 0 else 0.0
    return overall, read_gc


def gc_distribution(read_gc):
    # read별 GC%를 정수로 반올림해 센다. dist[p] = GC가 p% 인 read 수
    # 평균·중앙값은 반올림 전 값으로 구한다 (반올림 값으로 구하면 치우친다)
    dist = [0] * 101
    for g in read_gc:
        p = round(g * 100)
        dist[p] = dist[p] + 1
    return dist


def median(values):
    # 정렬한 뒤 가운데 값(짝수 개면 가운데 두 값의 평균)
    v = sorted(values)
    n = len(v)
    if n % 2 == 1:
        return v[n // 2]
    return (v[n // 2 - 1] + v[n // 2]) / 2


def test():
    # 손으로 계산할 수 있는 작은 예로 확인한다
    reads = [("r1", "GGCC", "IIII"), ("r2", "ATGC", "IIII"), ("r3", "AT", "II")]
    overall, read_gc = gc_summary(reads)
    assert overall == 6 / 10, overall     # G·C 6개 / 염기 10개
    assert read_gc == [1.0, 0.5, 0.0], read_gc
    dist = gc_distribution(read_gc)
    assert dist[100] == 1 and dist[50] == 1 and dist[0] == 1 and sum(dist) == 3
    assert median(read_gc) == 0.5
    assert abs(median([0.2, 0.4]) - 0.3) < 1e-12


test()

if len(sys.argv) < 2:
    print("사용법: python3 src/gc_content.py <FASTQ 파일> [분포 TSV]")
    sys.exit(1)

reads = read_fastq(sys.argv[1])
overall, read_gc = gc_summary(reads)
dist = gc_distribution(read_gc)

print("read 개수:", len(reads))
print(f"전체 GC 함량: {overall * 100:.2f}%")
print(f"read별 GC% 평균: {sum(read_gc) / len(read_gc) * 100:.2f}%")
print(f"read별 GC% 중앙값: {median(read_gc) * 100:.2f}%")
print(f"read별 GC% 범위: {min(read_gc) * 100:.2f}% ~ {max(read_gc) * 100:.2f}%")

# 두 번째 인자를 주면 GC% 분포를 TSV로 저장한다
if len(sys.argv) >= 3:
    with open(sys.argv[2], "w") as out:
        out.write("gc_percent\treads\n")
        for p in range(101):
            out.write(f"{p}\t{dist[p]}\n")
    print("저장:", sys.argv[2])
