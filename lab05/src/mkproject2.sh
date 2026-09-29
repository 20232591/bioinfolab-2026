#!/usr/bin/bash
#같은 이름의 폴더가 있는지 확인하고 같은 이름의 폴더가 있다면 오류메세지를 낸 뒤 끝낸다.
set -x

NAME=$1
mkdir $NAME
echo "$NAME 폴더를 만들었습니다"

if [ -z "$1" ]
then
    echo "<사용법>"
    exit 1
fi
 
if [ -d "$1" ] 
then 
  echo " 오류: 폴더가 이미 있습니다."
exit 1

fi 

