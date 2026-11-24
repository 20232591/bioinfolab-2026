import sys
from parse_gff import read_gff

# GFF 파일에서 CDS 만 골라 길이와 방향을 분석한다
features = read_gff(sys.argv[1])

# 1. type 이 CDS 인 주석만 골라낸다
cds_list = []
for f in features:
    if f["type"] == "CDS":
        cds_list.append(f)

# 2. 각 CDS 의 길이를 end - start + 1 로 계산한다
for f in cds_list:
    f["length"] = f["end"] - f["start"] + 1

lengths = [f["length"] for f in cds_list]

# 3. 개수, 평균 길이, 최소 길이, 최대 길이
print("CDS 개수:", len(cds_list))
print("평균 길이:", round(sum(lengths) / len(lengths), 1))
print("최소 길이:", min(lengths))
print("최대 길이:", max(lengths))
# 평균 길이를 3으로 나눈 평균 아미노산 개수 (세균 단백질은 대략 300 근처)
print("평균 아미노산 개수:", round(sum(lengths) / len(lengths) / 3, 1))

# 4. 정방향(+)과 역방향(-) 개수
plus = 0
minus = 0
for f in cds_list:
    if f["strand"] == "+":
        plus = plus + 1
    elif f["strand"] == "-":
        minus = minus + 1
print("정방향(+):", plus)
print("역방향(-):", minus)

# 5. 가장 긴 CDS 다섯 개의 좌표와 attributes
print()
print("가장 긴 CDS 5개")
longest = sorted(cds_list, key=lambda f: f["length"], reverse=True)[:5]
for f in longest:
    print(f["seqid"], f["start"], f["end"], f["strand"], f["length"], f["attributes"], sep="\t")
