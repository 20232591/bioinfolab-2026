# fasta.py 함수 목록

## read_fasta(filename)
- 받는 것: FASTA 파일 경로
- 돌려주는 것: 서열 이름과 서열을 짝지은 딕셔너리
- 예: `seqs = read_fasta("data/seqs.fasta")`

## gc_content(seq)
- 받는 것: 서열 문자열
- 돌려주는 것: GC 비율 (0~1 사이 소수)
- 예: `gc = gc_content("ATGC")`

## write_fasta(seqs, filename)
- 받는 것: 서열 딕셔너리, 저장할 파일 경로
- 돌려주는 것: 없음 (파일로 저장)
- 예: `write_fasta(seqs, "doc/output.fasta")`

## reverse_complement(seq)
- 받는 것: 서열 문자열
- 돌려주는 것: 역상보 서열
- 예: `rc = reverse_complement("ATGC")`

## length_stats(seqs)
- 받는 것: 서열 딕셔너리
- 돌려주는 것: 서열 개수, 전체 길이, 평균 길이, 최단, 최장 딕셔너리
- 예: `stats = length_stats(seqs)`

## 아쉬운 점
- 소문자 서열을 자동으로 처리하지못한다.
- 서열의 개수를 직접 세야한다는 단점이 있다.
-replace를 연달아 쓰면 이미 바꾼 염기를 다시 바꾸는 문제가 발생한다. 