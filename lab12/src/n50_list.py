import sys

# contig 길이 목록으로 N50 을 계산한다
# 사용법: python3 src/n50_list.py 12 3 20 8 1 15 6


def n50(lengths):
    # 길이를 긴 것부터 정렬한다
    lengths = sorted(lengths, reverse=True)
    total = sum(lengths)
    half = total / 2

    # 긴 contig 부터 길이를 누적하다가 전체의 절반 이상이 되는 contig 의 길이가 N50
    running = 0
    for length in lengths:
        running = running + length
        if running >= half:
            return length


# 인자가 없으면 과제의 contig 길이를 쓴다
if len(sys.argv) > 1:
    lengths = [int(x) for x in sys.argv[1:]]
else:
    lengths = [12, 3, 20, 8, 1, 15, 6]

print("contig 길이:", lengths)
print("정렬:", sorted(lengths, reverse=True))
print("전체 길이:", sum(lengths), " 절반:", sum(lengths) / 2)
print("N50:", n50(lengths))
