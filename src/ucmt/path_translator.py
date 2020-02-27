# -*- coding: utf-8 -*-
from typing import Union
from pathlib import Path
import sys


class Translator:
    @staticmethod
    def _check_existence(path: Path) -> None:
        if path.exists():
            return
        else:
            sys.exit(1)

    @staticmethod
    def _to_pathlib_object(path: Union[str, Path]) -> Path:
        if isinstance(path, Path):
            return path.absolute()
        else:
            return Path(path).absolute()


class ConfigPath(Translator):
    def __init__(self, path: Union[str, Path], collect_dir: Union[str, Path]):
        self._path = self._to_pathlib_object(path)
        self._collect_dir = self._to_pathlib_object(collect_dir)

    def origin_path(self, check_exists=False) -> Path:
        if check_exists:
            self._check_existence(self._path)

        return self._path

    def collect_path(self, check_exists=False) -> Path:
        collect_path = self._collect_dir / self._path.name
        if check_exists:
            # ないなら，プログラムが終了する
            self._check_existence(collect_path)

        return collect_path


class DBFilter(Translator):
    def __init__(self, root_dir: Union[str, Path]):
        # ユーザディレクトリ内のファイル・ディレクトリを想定している
        # ルートディレクトリの存在確認が必要かも？
        self._root_dir = self._to_pathlib_object(root_dir)

    def apply_inward(self, path: Union[str, Path]) -> Path:
        abs_path = self._to_pathlib_object(path)

        self._check_existence(abs_path)

        try:
            relative_path = abs_path.relative_to(self._root_dir)
        # TODO: エラーメッセージを出力する
        # エラーは，オブジェクトが root ディレクトリ配下にないときに出る
        except ValueError:
            sys.exit(1)
        else:
            return relative_path

    def apply_outward(self, path: str) -> Path:
        return self._root_dir / path
