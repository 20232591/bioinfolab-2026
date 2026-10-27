#!/usr/bin/bash

if [ $# -ne 1 ]; then
    echo "사용법: $0 <디렉토리>" >&2
    exit 1
fi

DIR="$1"
ls "$DIR"
