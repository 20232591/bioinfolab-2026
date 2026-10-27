"""FASTA 파일 이름을 받아 서열 개수를 출력한다."""
import os
import sys

# fasta.py 는 lab07/src 에만 있으므로 그 폴더를 import 경로에 추가한다
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lab07", "src"))
from fasta import read_fasta

# 인자가 하나가 아니면 사용법을 알려주고 끝낸다
if len(sys.argv) != 2:
    print("Usage: python3 src/count_agent2.py <fasta_file>")
    sys.exit(1)

# read_fasta 가 돌려준 딕셔너리의 항목 수가 서열 개수이다
seqs = read_fasta(sys.argv[1])
print(len(seqs))
