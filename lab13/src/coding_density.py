import sys
from parse_gff import read_gff

# 사용법: python3 src/coding_density.py doc/prokka_out/sample.gff 180912
# GFF 의 CDS 길이를 모두 더해 1000 염기당 유전자 수와 코딩 밀도를 계산한다
gff_file = sys.argv[1]
genome_len = int(sys.argv[2])  # seqkit stats 의 sum_len

features = read_gff(gff_file)

# 1. CDS 만 골라 길이(end - start + 1)를 구한다
cds_lengths = []
for f in features:
    if f["type"] == "CDS":
        cds_lengths.append(f["end"] - f["start"] + 1)

n_cds = len(cds_lengths)
total_cds = sum(cds_lengths)

# 2. 1000 염기당 유전자 수
genes_per_kb = n_cds / genome_len * 1000

# 3. 코딩 밀도 = CDS 길이 총합 / 유전체 길이 * 100
density = total_cds / genome_len * 100

print()
print("유전체 전체 길이:", genome_len)
print("CDS 개수:", n_cds)
print("1000 염기당 유전자 수:", round(genes_per_kb, 3))
print("CDS 길이 총합:", total_cds)
print("코딩 밀도(%):", round(density, 2))
