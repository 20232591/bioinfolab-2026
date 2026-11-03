# lab07/src/fasta.py 함수 요약

- `read_fasta(filename)`: FASTA 파일을 읽어 `{이름: 서열}` 딕셔너리로 돌려준다. 헤더와 서열을 모두 대문자로 바꾸고, 헤더는 첫 단어만 이름으로 쓴다. 여러 줄로 나뉜 서열은 한 줄로 합친다.
- `write_fasta(seqs, filename)`: `{이름: 서열}` 딕셔너리를 FASTA 파일로 저장한다. 서열마다 `>이름` 한 줄과 서열 한 줄을 쓴다.
- `gc_content(seq)`: GC 비율을 0~1 사이의 수로 돌려준다. 빈 서열이면 0.0을 돌려준다.
- `reverse_complement(seq)`: A↔T, G↔C로 바꾼 뒤 뒤집어서 역상보 서열을 돌려준다.
- `length_stats(seqs)`: 서열 개수, 총길이, 평균 길이, 최소 길이, 최대 길이를 딕셔너리로 돌려준다.
- `__main__` 블록: 직접 실행하면 서열마다 이름, 길이, GC 비율을 출력하고, 역상보를 `assert` 로 테스트한다.
