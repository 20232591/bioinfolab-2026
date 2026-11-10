# qual_summary.py 사용 설명서

FASTQ 파일을 읽어 read마다 평균 품질 점수(Phred)를 구하고, 그 값들의 평균을 "전체 read 평균 품질"로 출력하는 스크립트이다.

- 위치: `lab11/src/qual_summary.py`
- 필요 환경: Python 3 (표준 라이브러리만 사용, 추가 설치 없음)

## 1. 사용법

주차 폴더(`lab11`)에서 실행한다. 인자로 FASTQ 파일 경로 하나를 준다.

```
cd lab11
python3 src/qual_summary.py <FASTQ 파일>
```

### 실행 예시

```
$ python3 src/qual_summary.py data/SRR1553607_1.fastq
전체 read 평균 품질: 33.4497222958299

$ python3 src/qual_summary.py data/SRR1553607_2.fastq
전체 read 평균 품질: 30.830840894308746

$ python3 src/qual_summary.py data/trimmed_1.fastq
전체 read 평균 품질: 34.9476925706938
```

| 파일 | read 수 | 전체 read 평균 품질 |
|---|---|---|
| SRR1553607_1.fastq (forward) | 203,445 | 33.45 |
| SRR1553607_2.fastq (reverse) | 203,445 | 30.83 |
| trimmed_1.fastq (fastp 처리 후) | 188,357 | 34.95 |

- reverse read(_2)가 forward read(_1)보다 평균 품질이 약 2.6 낮다. Illumina paired-end에서 흔히 보이는 경향이다.
- fastp로 품질 낮은 끝부분을 자르고 나쁜 read를 버린 뒤(trimmed_1) 평균 품질이 33.45 → 34.95로 올라갔다.

## 2. 품질 점수(Phred) 읽는 법

FASTQ의 4번째 줄은 염기마다 품질 점수를 문자 하나로 나타낸다. 이 데이터는 **Phred+33** 방식이다.

- 점수 = 문자의 ASCII 코드 - 33
- 점수 Q의 오류 확률 = 10^(-Q/10)

| 문자 | ASCII | 점수 Q | 오류 확률 |
|---|---|---|---|
| ! | 33 | 0 | 1 (100%) |
| + | 43 | 10 | 1/10 |
| 5 | 53 | 20 | 1/100 |
| ? | 63 | 30 | 1/1,000 |
| I | 73 | 40 | 1/10,000 |
| J | 74 | 41 | 1/12,600 |

보통 Q30 이상이면 품질이 좋다고 본다. 평균 33~35 는 염기 1,000개 중 오류가 1개보다 적은 수준이다.

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
3. 1번째 줄에서 줄바꿈과 맨 앞 `@` 를 떼어 이름으로, 2번째 줄을 서열로, 4번째 줄을 품질 문자열로 쓴다. 3번째 줄(`+`)은 건너뛴다.
4. `(이름, 서열, 품질)` 튜플의 리스트를 돌려준다. (`parse_fastq.py` 의 함수와 같다.)

### mean_quality(qual)

```python
def mean_quality(qual):
    scores = []
    for ch in qual:
        scores.append(ord(ch) - 33)
    return sum(scores) / len(scores)
```

1. 품질 문자열의 문자 하나하나를 `ord(ch)` 로 ASCII 코드로 바꾼다.
2. 33을 빼서 Phred 점수로 만들고 `scores` 에 모은다.
3. 점수 합 ÷ 염기 수 = 그 read의 평균 품질을 돌려준다.

예: 첫 read(`SRR1553607.1`, 101 bp)의 품질 문자열 `BB@FFFFFHHHHHJJJ...` 는 평균 37.44 이다.

### 메인 부분

```python
reads = read_fastq(sys.argv[1])

total = 0
for name, seq, qual in reads:
    q = mean_quality(qual)
    total = total + q

print("전체 read 평균 품질:", total / len(reads))
```

- `sys.argv[1]` : 명령줄에서 받은 첫 번째 인자(파일 경로)
- 반복문에서 read마다 평균 품질을 구해 `total` 에 더한다.
- `total / len(reads)` : read별 평균 품질들의 평균을 출력한다.

## 4. 출력 값의 의미

출력값은 **read별 평균 품질의 평균**이다. 모든 염기의 품질을 한꺼번에 평균한 값과는 다를 수 있다.

- 원본 파일처럼 read 길이가 모두 같으면(101 bp) 두 값이 같다. SRR1553607_1: 33.4497 (두 방식 모두)
- fastp로 자른 파일처럼 read 길이가 제각각이면(50~101 bp) 짧은 read도 긴 read와 같은 무게로 계산되어 값이 달라진다. trimmed_1: read별 평균의 평균 34.948, 염기 전체 평균 34.912

결과는 화면에 출력된다. 파일로 저장하려면 리다이렉션을 쓴다.

```
python3 src/qual_summary.py data/SRR1553607_1.fastq > doc/qual_result.txt
```

## 5. 결과 검증

FastQC 보고서(`doc/SRR1553607_1_fastqc.html`)의 "Per sequence quality scores" 그래프에서 read별 평균 품질 분포를 볼 수 있다. 분포의 중심이 33~34 근처인지 비교한다. 서열 분석 환경에서는 seqkit으로도 확인할 수 있다.

```
seqkit stats -a data/SRR1553607_1.fastq    # AvgQual 열
```

## 6. 주의할 점과 한계

- **인자를 주지 않으면** `IndexError: list index out of range` 가 난다 (`sys.argv[1]` 이 없음).
- **빈 파일**이면 `len(reads)` 가 0이라 `ZeroDivisionError` 가 난다. 품질 문자열이 빈 read가 있어도 `mean_quality` 에서 같은 오류가 난다.
- **Phred+33 만 가정**한다. 오래된 Illumina(1.3~1.7)의 Phred+64 파일은 점수가 31씩 높게 나온다.
- **한 read가 정확히 4줄**이라고 가정한다. 여러 줄로 나뉜 FASTQ나 잘린 파일은 처리하지 못한다.
- **파일 전체를 메모리에 올린다** (`readlines()`). 수 GB 크기의 FASTQ에서는 메모리가 부족할 수 있다.
- **gzip 압축 파일**(`.fastq.gz`)은 바로 읽지 못한다. 먼저 압축을 풀어야 한다.
- 평균만 출력하므로 품질이 낮은 read가 얼마나 있는지(분포, 최솟값, Q30 이상 비율 등)는 알 수 없다.
