# lab07 요약 — 함수와 파일 저장

## 목표
- 반복되는 코드를 **함수**로 묶고, 함수를 모은 **모듈**(`fasta.py`)을 만들어 여러 스크립트에서 `import`해서 쓴다.
- 결과를 화면 출력이 아니라 **파일(TSV, FASTA)로 저장**한다.

## 폴더 구조
```
lab07/
├── data/   seqs.fasta, seqs2.fasta, lower.fasta   (입력 서열)
├── doc/    python_cheatsheet.md, summary.tsv, batchinfo.tsv, long.fasta (결과물·정리)
└── src/    fasta.py(모듈) + 이를 사용하는 스크립트들, README.md(함수 설명)
```

## 1. 함수 기초
```python
def 함수이름(받을값):
    """설명(docstring)"""
    return 결과
```
- `fgc.py`: `gc_content(seq)`를 처음 함수로 만들어 호출해 봄
- `fseqlen.py`: **print vs return** 비교
  - `print`: 화면에 보여주고 끝 → 함수 값은 `None`
  - `return`: 값을 돌려주어 다음 코드에서 쓸 수 있음
- `help(gc_content)`로 docstring 확인 (`sew` 파일에 출력 결과 저장)

## 2. 모듈 `src/fasta.py`
| 함수 | 받는 것 | 돌려주는 것 |
|---|---|---|
| `read_fasta(filename)` | FASTA 파일 경로 | `{이름: 서열}` 딕셔너리 |
| `write_fasta(seqs, filename)` | 서열 딕셔너리, 저장 경로 | 없음 (파일 저장) |
| `gc_content(seq)` | 서열 문자열 | GC 비율 (0~1), 빈 서열이면 0.0 |
| `reverse_complement(seq)` | 서열 문자열 | 역상보 서열 |
| `length_stats(seqs)` | 서열 딕셔너리 | count, total, mean, min, max 딕셔너리 |

- `if __name__ == "__main__":` 아래 코드는 **직접 실행할 때만** 동작, `import` 될 때는 실행되지 않음
- 테스트: `assert reverse_complement(reverse_complement(seq)) == seq`
- 다른 스크립트에서 사용: `from fasta import read_fasta, gc_content`

## 3. 모듈을 사용하는 스크립트
| 스크립트 | 사용법 | 하는 일 |
|---|---|---|
| `countseq2.py` | `python3 src/countseq2.py FASTA` | 서열 개수 출력 |
| `seqlen2.py` | `python3 src/seqlen2.py FASTA` | 서열별 길이 출력 |
| `stats.py` | `python3 src/stats.py FASTA` | `length_stats`로 길이 통계 출력 |
| `summary.py` | `python3 src/summary.py FASTA OUT.tsv` | 서열별 name/length/gc를 TSV로 저장 |
| `filter_fasta.py` | `python3 src/filter_fasta.py FASTA 최소길이 OUT.fasta` | 최소 길이 이상 서열만 FASTA로 저장 |
| `batchinfo2.py` | `python3 src/batchinfo2.py 폴더 OUT.tsv` | 폴더 안 모든 `*.fasta`의 개수/총길이/평균GC를 TSV로 저장 (`glob` 사용) |
| `filter.py` | `python3 src/filter.py FASTA` | (모듈 이전 방식) 길이 20~40, GC 0.4~0.6 서열만 출력 |

### 결과 예시
`doc/summary.tsv`
```
name   length  gc
GENE1  34      0.4412
GENE2  17      0.4118
GENE3  24      0.5
```
`doc/batchinfo.tsv`
```
filename          count  total  mean_gc
data/seqs2.fasta  2      16     0.25
data/seqs.fasta   3      67     0.504
```

## 4. 파일 쓰기
- `open(파일, "w")`: 새로 쓰기 → bash의 `>`
- `open(파일, "a")`: 이어 쓰기 → bash의 `>>`
- 숫자는 `str()`로 바꿔서 쓰고, 열 구분은 `\t`, 줄 끝은 `\n`

## 5. 소문자 서열 문제 (`lower.fasta`)
- 소문자 서열은 `count("G")`에 잡히지 않아 GC 비율이 틀리게 나옴
- `read_fasta`에서 `line.upper()`를 적용해 대문자로 통일
- 모듈 하나만 고치면 `countseq2.py`, `seqlen2.py` 등 import 하는 모든 스크립트에 반영됨 → lab06처럼 스크립트마다 코드를 복사했다면 파일마다 각각 고쳐야 함

> ⚠️ 주의: 처음에는 `rstrip()`을 `upper()`로 **바꿔서** 줄바꿈/공백이 서열에 남았고,
> GENE1 길이가 30이 아니라 34로 나왔다. → `line = line.rstrip().upper()`처럼 **둘 다** 쓰도록 수정함.

## 6. 겪은 오류
| 오류 | 원인 |
|---|---|
| `ZeroDivisionError` | 빈 서열로 GC 비율 계산 → `len(seq) == 0` 검사 추가 |
| `TypeError` (None 연산) | `print`만 하고 `return` 안 한 함수의 결과(None)로 연산 |
| `TypeError: '>=' not supported between 'int' and 'str'` | `sys.argv`는 문자열 → `int(sys.argv[2])` 필요 |

## 7. 아쉬운 점 (README 기록)
- 소문자 서열을 자동으로 처리하지 못했음 (→ `upper()`로 수정)
- `replace`를 연달아 쓰면 이미 바꾼 염기를 다시 바꾸는 문제 → 역상보는 딕셔너리 `table`로 해결
