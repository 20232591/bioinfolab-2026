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


def read_id(name):
    # 헤더에서 공백 앞 첫 단어만 쓰고, 끝의 /1 · /2 는 떼어 낸다
    # 예: "SRR1553607.1 1 length=101" -> "SRR1553607.1", "r1/2" -> "r1"
    rid = name.split()[0] if name.strip() else ""
    if rid.endswith("/1") or rid.endswith("/2"):
        rid = rid[:-2]
    return rid


def check_pairs(reads1, reads2):
    # 같은 순서의 read 이름이 서로 맞는지 확인한다
    # 반환: (짝이 맞는 수, 짝이 안 맞는 (번호, 이름1, 이름2) 리스트)
    matched = 0
    mismatches = []
    for i in range(min(len(reads1), len(reads2))):
        id1 = read_id(reads1[i][0])
        id2 = read_id(reads2[i][0])
        if id1 == id2:
            matched = matched + 1
        else:
            mismatches.append((i + 1, id1, id2))
    return matched, mismatches


def test():
    # 손으로 확인할 수 있는 작은 예
    assert read_id("SRR1553607.1 1 length=101") == "SRR1553607.1"
    assert read_id("r1/1") == "r1" and read_id("r1/2") == "r1"
    r1 = [("a/1", "AC", "II"), ("b/1", "GT", "II"), ("c/1", "AA", "II")]
    r2 = [("a/2", "GT", "II"), ("x/2", "AC", "II")]
    matched, mism = check_pairs(r1, r2)
    assert matched == 1, matched
    assert mism == [(2, "b", "x")], mism


test()

if len(sys.argv) < 3:
    print("사용법: python3 src/check_paired.py <R1 FASTQ> <R2 FASTQ>")
    sys.exit(1)

reads1 = read_fastq(sys.argv[1])
reads2 = read_fastq(sys.argv[2])
matched, mismatches = check_pairs(reads1, reads2)

print("R1 read 개수:", len(reads1))
print("R2 read 개수:", len(reads2))
print("짝이 맞는 read 수:", matched)
print("이름이 다른 read 수:", len(mismatches))

# 이름이 다른 read는 처음 5개만 보여 준다
for num, id1, id2 in mismatches[:5]:
    print(f"  {num}번째: {id1} != {id2}")

# 개수가 같고 모든 이름이 짝을 이루어야 올바른 쌍이다
if len(reads1) == len(reads2) and not mismatches:
    print("결과: 두 파일은 올바른 paired-end 쌍이다")
else:
    print("결과: 두 파일의 짝이 맞지 않는다")
