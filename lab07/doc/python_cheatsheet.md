
# Python Cheatsheet

## 스크립트를 만드는 다섯 단계
단계 | 할 일 | bash 예 | 파이썬 예
1 | 터미널에서 직접 실행 | `grep -c ">" data/seqs.fasta` | `python3 -c "..."` 
2 | 파일에 옮겨 실행 | `bash src/countseq.sh` | `python3 src/countseq.py`
3 | 바뀔 값을 변수로 | `FILE="data/seqs.fasta"` | `file = "data/seqs.fasta"`
4 | 변수를 인자로 받기 | `FILE="$1"` | `file = sys.argv[1]`
5 | 인자 검사 붙이기 | `if [ -z "$1" ]` | `if len(sys.argv) < 2:`

## 따옴표와 변수
형태 | bash | 파이썬
변수 만들기 | `NAME=gene1` (= 앞뒤 공백 없음) | `name = "gene1"`
변수 쓰기 | `"$NAME"` | `name`
글자 그대로 | `'$NAME'` | 파이썬에선 차이 없음

## 종료 상태
- bash: `echo $?` → 0이 성공
- 파이썬으로 옮길 필요 없음 (파이썬은 오류시 예외 발생)

## 디버깅
- bash: `set -x`
- 파이썬: `print()`으로 중간값 확인

## 내가 실수했던 것
- `$` 까지 입력함 → 프롬프트 표시이지 입력하는 글자가 아님
- 실행 권한을 안 줌 → `chmod +x`
- shebang을 잘못 씀 → `#!/usr/bin/env python3`
- 파이썬은 shebang 없이 `python3 src/script.py`로 실행

## 실행 방법 비교
방법 | bash | 파이썬
권한 없이 | `bash src/a.sh` | `python3 src/a.py`
직접 실행 | `./src/a.sh` (chmod 필요) | `./src/a.py` (chmod 필요)

## 07번 - 함수와 파일 저장

### 함수 만들기 
def 함수이름(받을값):
    """설명"""
    return 결과

### print vs return
- print: 화면에 보여주고 끝 (None 반환)
- return: 다음 코드에 값을 넘겨줌

### 모듈 불러오기
from fasta import read_fasta

### if __name__ == "__main__"
파일을 직접 실행할 때만 실행되는 코드를 넣을 때 씀
다른 스크립트에서 import 할 때는 실행되지 않음

### 파일 쓰기
- open(파일, "w") : 새로 쓰기 → bash의 >
- open(파일, "a") : 이어 쓰기 → bash의 >>

### 오늘 겪은 오류
1. ZeroDivisionError: 빈 서열로 GC 비율 계산할 때
2. TypeError: None에 연산 시도할 때