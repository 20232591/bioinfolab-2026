# parse_fastq.py 사용 설명서

FASTQ 파일을 읽어 read 개수와 첫 번째 read의 이름·서열·길이를 출력하는 스크립트이다.

- 위치: `lab11/src/parse_fastq.py`
- 필요 환경: Python 3 (표준 라이브러리만 사용, 추가 설치 없음)

## 1. 사용법

주차 폴더(`lab11`)에서 실행한다. 인자로 FASTQ 파일 경로 하나를 준다.

```
cd lab11
python3 src/parse_fastq.py <FASTQ 파일>
```

### 실행 예시

```
$ python3 src/parse_fastq.py data/SRR1553607_1.fastq
read 개수: 203445
첫 read 이름: SRR1553607.1 1 length=101
첫 read 서열: GTTAGCGTTGTTGATCGCGACGCAACAACTGGTAAAGAATCTGGAAGAAGGATATCAGTTCAAACGCTCAAGCGAGATGATGGATATTTTTGAACGACTCA
첫 read 길이: 101
```

fastp로 정리한 파일에도 똑같이 쓸 수 있다.

```
$ python3 src/parse_fastq.py data/trimmed_1.fastq
read 개수: 188357
첫 read 이름: SRR1553607.1 1 length=101
...
```

두 결과를 비교하면 트리밍·필터링으로 read가 203,445개에서 188,357개로 15,088개(약 7.4%) 줄었음을 알 수 있다.

## 2. 입력 형식: FASTQ

FASTQ는 read 하나를 **4줄**로 나타낸다.

| 줄 | 내용 | 예 |
|---|---|---|
| 1 | `@` + read 이름 | `@SRR1553607.1 1 length=101` |
| 2 | 염기 서열 | `GTTAGCGTTG...` |
| 3 | `+` (이름이 반복되기도 함) | `+SRR1553607.1 1 length=101` |
| 4 | 품질 점수(서열과 같은 길이) | `BB@FFFFFHH...` |

## 3. 코드 설명

### read_fastq(filename)

```python
def read_fastq(filename):
    records = []
    with open(filename) as f:
        lines = f.readlines()

    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))

    return records
```

1. `f.readlines()` 로 파일 전체를 줄 단위 리스트로 읽는다.
2. `range(0, len(lines), 4)` 로 4줄씩 건너뛰며 read 하나씩 처리한다.
3. `lines[i]` (1번째 줄): `rstrip()` 으로 줄바꿈을 지우고 `[1:]` 로 맨 앞 `@` 를 뗀다 → 이름
4. `lines[i + 1]` (2번째 줄): 서열
5. `lines[i + 2]` (3번째 줄, `+`): 쓰지 않으므로 건너뛴다.
6. `lines[i + 3]` (4번째 줄): 품질 문자열
7. `(이름, 서열, 품질)` 튜플을 `records` 리스트에 모아 돌려준다.

### 반환값

`[(name, seq, qual), ...]` 형태의 리스트. 예를 들어

- `reads[0][0]` : 첫 read 이름
- `reads[0][1]` : 첫 read 서열
- `reads[0][2]` : 첫 read 품질 문자열

### 메인 부분

```python
reads = read_fastq(sys.argv[1])
print("read 개수:", len(reads))
print("첫 read 이름:", reads[0][0])
print("첫 read 서열:", reads[0][1])
print("첫 read 길이:", len(reads[0][1]))
```

- `sys.argv[1]` : 명령줄에서 받은 첫 번째 인자(파일 경로)
- `len(reads)` : 전체 read 개수
- `len(reads[0][1])` : 첫 read 서열의 길이(염기 수)

## 4. 출력 항목

| 출력 | 의미 |
|---|---|
| read 개수 | 파일 안의 전체 read 수 (= 줄 수 ÷ 4) |
| 첫 read 이름 | `@` 를 뺀 첫 번째 헤더 줄 |
| 첫 read 서열 | 첫 번째 read의 염기 서열 |
| 첫 read 길이 | 첫 번째 read 서열의 염기 수 |

결과는 화면에 출력된다. 파일로 저장하려면 리다이렉션을 쓴다.

```
python3 src/parse_fastq.py data/SRR1553607_1.fastq > doc/parse_result.txt
```

## 5. 결과 검증

read 개수는 셸 명령이나 seqkit 결과와 맞는지 확인할 수 있다.

```
echo $(( $(wc -l < data/SRR1553607_1.fastq) / 4 ))   # 203445
seqkit stats data/SRR1553607_1.fastq                  # 서열 분석 환경에서만
```

## 6. 주의할 점과 한계

- **인자를 주지 않으면** `IndexError: list index out of range` 가 난다 (`sys.argv[1]` 이 없음).
- **빈 파일**이면 `reads[0]` 이 없어 마찬가지로 `IndexError` 가 난다.
- **한 read가 정확히 4줄**이라고 가정한다. 서열이 여러 줄로 나뉜 FASTQ나 줄 수가 4의 배수가 아닌(잘린) 파일은 처리하지 못한다.
- **파일 전체를 메모리에 올린다** (`readlines()`). 이 실습의 파일(약 20만 read)은 문제없지만, 수 GB 크기의 FASTQ에서는 메모리가 부족할 수 있다.
- **gzip 압축 파일**(`.fastq.gz`)은 바로 읽지 못한다. 먼저 압축을 풀어야 한다.
- 품질 문자열(`qual`)은 읽어 두지만 출력에는 쓰지 않는다. 평균 품질 계산 등으로 확장할 수 있다.
- `read_fasta` (lab07)와 달리 이름·서열을 대문자로 바꾸지 않고 원래대로 둔다.
