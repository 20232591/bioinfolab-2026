#!/usr/bin/bash
# batchinfo.sh — 폴더 안의 모든 FASTA 파일의 이름과 서열 개수를 탭으로 구분해 출력한다
# 사용법: batchinfo.sh <폴더>

if [ ! -d "$1" ]
then
    echo "사용법: $0 <폴더>"
    exit 1
fi



for F in "$1"/*.fasta
do
   echo $F
   grep -c ">" "$F"
done



