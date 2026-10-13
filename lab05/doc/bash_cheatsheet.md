
스크립트를 만드는 다섯 단계
단계	할 일	예 (countseq.sh)
1	터미널에서 명령어 직접 실행	`grep -c ">" data/seqs.fasta`
2	그대로 파일에 옮겨 `bash`로 실행	`bash src/countseq.sh`
3	바뀔 값을 변수로	`FILE="data/seqs.fasta"`
4	변수를 `$1`로 받기	`FILE="$1"`
5	인자·파일 검사 붙이기	아래 "검사" 참고
순서를 지키는 이유: 1단계에서 되면, 이후 오류는 전부 스크립트 쪽 문제다.
검사 (5단계)
```bash
if [ -z "$1" ]          # 인자가 비었으면
then
    echo "사용법: $0 <FASTA파일>"
    exit 1              # 실패로 끝내기
fi
if [ ! -f "$1" ]        # 파일이 없으면
then
    echo "오류: 파일을 찾을 수 없습니다: $1"
    exit 1
fi
```
`[` 바로 안쪽·바깥쪽에 공백 필수: `[ -z "$1" ]` (O), `[-z "$1"]` (X)
폴더 확인은 `-d`: `[ -d "$NAME" ]`
따옴표와 변수
형태	의미	예
`"$NAME"`	값으로 바뀜 (기본으로 이것)	`mkdir "$NAME"`
`'$NAME'`	글자 그대로	`echo '$NAME'` → `$NAME`
`$NAME`	공백에서 쪼개짐 (쓰지 않기)	`mkdir $NAME` → 폴더 2개
변수 만들 때 `=` 앞뒤 공백 없음: `NAME=gene1` (`NAME = gene1`은 오류)
종료 상태
`echo $?` → 직전 명령어 결과. 0이 성공, 0이 아니면 실패.
`grep`은 화면에 아무것도 안 나와도 못 찾으면 1이다.
디버깅
오류 메시지는 마지막 줄부터: 어느 파일 / 몇 번째 줄 / 무엇에 대해 / 어떤 문제
`set -x`를 스크립트 두 번째 줄에 넣으면 실행되는 명령어가 `+`로 찍힌다. 해결되면 지운다.
내가 실수했던 것
`$`까지 같이 입력함
`$ ./src/mkproject.py` → `bash: $: command not found`
`$`는 프롬프트 표시이지 입력하는 글자가 아니다. → `./src/mkproject.py`
실행 권한을 안 줌
`./src/mkproject.py` → `Permission denied`
→ `chmod +x src/mkproject.py` (수업에서는 `chmod 700`)
shebang을 잘못 씀 / 빠뜨림
첫 줄이 없으면 bash가 코드를 명령어로 읽음: `import: command not found`
`#!/usr/bin/env/python3`처럼 `env` 뒤에 `/`를 쓰면 `bad interpreter: Not a directory`
→ 올바른 형태: `#!/usr/bin/env python3` (공백)
실행 방법 비교
방법	조건
`bash src/a.sh`	권한·shebang 없어도 됨
`./src/a.sh`	`chmod` 권한 + 첫 줄 shebang 필요
