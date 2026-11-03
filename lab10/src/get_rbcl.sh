#!/bin/bash
# 식물 8종의 rbcL 서열을 NCBI E-utilities(esearch, efetch)로 받는다.
# 실행: cd lab10 && bash src/get_rbcl.sh
BASE="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# 학명|파일 이름
# 인삼(Panax ginseng)은 rbcL 이 엽록체 유전체 전체(약 15만 bp)로만 올라 있어
# 1300:1500[SLEN] 조건으로는 0건이다. 그래서 속(Panax)으로 검색해
# 같은 속인 미국삼(Panax quinquefolius, U50250)의 rbcL 을 대신 받는다.
SPECIES="Arabidopsis thaliana|rbcL_arabidopsis
Panax|rbcL_ginseng
Oryza sativa|rbcL_rice
Zea mays|rbcL_maize
Ginkgo biloba|rbcL_ginkgo
Pinus thunbergii|rbcL_pine
Adiantum capillus-veneris|rbcL_fern
Marchantia polymorpha|rbcL_liverwort"

echo "$SPECIES" | while IFS='|' read -r NAME FILE; do
    # 검색어: 종 + rbcL 유전자 + 길이 1300~1500
    TERM="\"$NAME\"[ORGN] AND rbcL[GENE] AND 1300:1500[SLEN]"
    TERM_URL=$(echo "$TERM" | sed 's/ /+/g; s/"/%22/g')

    # esearch 결과의 첫 번째 ID만 꺼낸다
    ID=$(wget -q -O - "$BASE/esearch.fcgi?db=nuccore&retmax=1&term=$TERM_URL" \
         | grep -o '<Id>[0-9]*</Id>' | head -1 | sed 's/<[^>]*>//g')
    sleep 1

    if [ -z "$ID" ]; then
        echo "$NAME: 검색 결과 없음"
        continue
    fi
    echo "$NAME -> ID $ID -> $FILE"

    # FASTA 와 GenBank 를 받는다
    wget -q -O "data/$FILE.fa" "$BASE/efetch.fcgi?db=nuccore&id=$ID&rettype=fasta&retmode=text"
    sleep 1
    wget -q -O "data/$FILE.gb" "$BASE/efetch.fcgi?db=nuccore&id=$ID&rettype=gb&retmode=text"
    sleep 1
done
