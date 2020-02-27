# -*- coding: utf-8 -*-
import os
from pathlib import Path
import sys

# 現在作成中のライブラリ群にパスを通す
sys.path.append(os.getcwd() + "/src")

os.chdir(Path(__file__).parent)
