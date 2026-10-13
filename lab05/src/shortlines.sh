import sys
import os

# 1. 인자가 둘 다 있는지 검사
if len(sys.argv) < 3:
    print(f"사용법: {sys.argv[0]} <FASTA파일> <최소길이>")
    sys.exit(1)

file_path = sys.argv[1]
length_str = sys.argv[2]

# 파일 존재 여부 검사 (Bash의 [ ! -f "$1" ] 대응)
if not os.path.isfile(file_path):
    print(f"오류: 파일을 찾을 수 없습니다: {file_path}")
    sys.exit(1)

# 2. 두 번째 인자가 숫자인지 확인 (isdigit 사용)
if not length_str.isdigit():
    print(f"오류: 최소 길이는 숫자여야 합니다: {length_str}")
    sys.exit(1)

# 3. 글자로 들어온 두 번째 인자를 int()로 숫자 변환
length = int(length_str)

# 4. 서열 줄 세기 (Bash의 grep -v ">" 방식 구현)
n = 0
with open(file_path, "r") as f:
    for line in f:
        line = line.strip()
        # 빈 줄이 아니고 헤더(>)가 아닌 서열 줄만 계산
        if line and not line.startswith(">"):
            # Bash의 ${#LINE} -lt "$LENGTH" 대응
            if len(line) < length:
                n += 1

print(n)