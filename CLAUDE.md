# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# 이 저장소의 규칙

## 이 저장소는
생물정보학실험 수업의 실습 저장소이다. 주차별로 labNN 폴더가 있다.

- 새 주차 폴더는 `cp -r lab-template labNN` 으로 만든다. 폴더마다 `data/`(입력·내려받은 데이터), `doc/`(결과·보고서), `src/`(스크립트)를 둔다. 결과 파일은 `doc/` 에 쓴다.
- `resources/` 는 수업에서 나눠 준 원본 데이터·스크립트이다.
- fastq·sra 파일과 shovill·prokka 결과 폴더는 `.gitignore` 에 있어 저장소에 없다. 필요하면 wget 으로 다시 받는다.
- 도구는 Codespace 환경(`.devcontainer/1-basic`~`4-genome`)마다 다르다: 기본(02~07주차, 파이썬만), conda 실습(micromamba), 서열 분석(08~09·12~14주차, seqkit·blast·mafft·iqtree·fastqc·fastp), 유전체(10~11주차, + shovill·prokka).

## 실행 방법
주차 폴더에서 실행한다. 경로는 주차 폴더 기준이다.

```
cd lab07
python3 src/summary.py data/seqs.fasta doc/summary.tsv

cd ../lab05
bash src/countseq.sh data/seqs.fasta
```

테스트 프레임워크는 없다. `python3 src/fasta.py data/lower.fasta` 가 assert 테스트를 겸한다.

## 코드를 쓸 때
- FASTA 파일은 lab07/src/fasta.py 의 read_fasta 로 읽는다.
  - `from fasta import ...` 는 `lab07/src/` 안에서만 된다. 다른 주차에는 `fasta.py` 가 없다.
  - 다른 주차에서 쓸 때는 `fasta.py` 를 복사하지 말고 `lab09/src/count_agent2.py` 처럼 `sys.path` 에 `lab07/src` 를 추가한다.
  - read_fasta 는 헤더(서열 이름)까지 대문자로 바꾼다.
  - 예외: lab05·lab06 스크립트, lab07 의 `filter.py`·`fgc.py`·`fseqlen.py` 는 직접 읽기·함수 정의 연습용이다. read_fasta 로 바꾸지 않는다.
- 새 라이브러리(Biopython 등)를 쓰기 전에 먼저 물어본다.
- 주석은 한국어로 쓴다.
- seqkit, blast 등이 없으면 설치하지 말고 알린다 (저장소 루트에서 `bash .devcontainer/check.sh` 로 확인). conda 실습 주차만 예외.
- 코드 수정 후에는 정상적으로 코드가 실행되는지 테스트 코드를 실행한다.
-반복해서 받을 때는 요청 사이에 sleep 1을 넣는다.
-유전자 하나를 받을 때는 [SLEN]으로 길이를 제한한다.
-검색 결과가 없으면 검색어를 바꾸지 말고 먼저 알려준다.
-받은 파일마다 VERSION과 ORGANISM을 확인하고 알려준다.
-wget과 E-utilities를 쓴다. 주슨 반드시 큰 따옴표로 감싼다.
ㅣ
## 하지 말 것
- rm 으로 파일을 지우지 않는다.
- pip install 로 무언가를 설치하지 않는다.
- git 명령어를 실행하지 않는다.
- 스크립트 아래쪽의 `#` 주석(실행 결과, 과제 답안)을 지우거나 고치지 않는다.
-서열 파일을 읽을 때 Biopython 의 seqIO를 써도 된다.
-그 밖의 새 라이브러리는 쓰기 전에 물어본다.
