#!/usr/bin/env python3

import os
import sys

if len(sys.argv) < 2:
    print(f"사용법: {sys.argv[0]}, <폴더명>")
    sys.exit(1)


name = sys.argv[1]

if os.path.isdir(name):
    print(f"오류: 이미 존재하는 폴더입니다: {name}")
    sys.exit(1)

os.makedirs(os.path.join(name, "data"))
os.makedirs(os.path.join(name, "doc"))
os.makedirs(os.path.join(name, "src"))
print(f"프로젝트 폴더를 만들었습니다: {name}")
