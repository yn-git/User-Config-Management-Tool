# -*- coding: utf-8 -*-
import os
from pathlib import Path

import pytest

os.chdir(Path(__file__).parent)


class Maker():
    """指定した root_dir 配下にファイル・ディレクトリを生成する

    Args:
        root_dir (str):
            テスト用のファイル・ディレクトリを格納するディレクトリの path

    Attributes:
        root_dir (str):
            テスト用のファイル・ディレクトリを格納するディレクトリの path
        make_file_count (int):
            自動生成したファイル名の数
            ファイル命名の prefix として使用
        make_dir_count (int):
            自動生成したディレクト名の数
            命名の prefix として使用
    """

    def __init__(self, root_dir: Path):
        self._root_dir = root_dir
        self._make_file_count: int = 0
        self._make_dir_count: int = 0

    @property
    def root_dir(self):
        return str(self._root_dir)

    def make_file(
            self, *, parent_dir: str = None, filename: str = None) -> Path:
        """テスト用のファイルを作成する

        Args:
            parent_dir (str, optional):
                親ディレクトリの指定
                指定がなければ，root_dir 直下に作成する．
            filename (str, optional):
                ファイル名はクラス生成時に指定したディレクトリを root とした
                相対パスで指定する．
                指定がなければ，自動的にファイル名を生成する
                生成されるファイル名 testfile_<作成された回数(0 から)>

        Returns:
            Path: 生成したファイルの pathlib オブジェクト
        """
        if filename is None:
            test_file_name \
                = "testfile_" + str(self._make_file_count)
            self._make_file_count += 1
        else:
            test_file_name = filename

        if parent_dir is None:
            test_file = self._root_dir / test_file_name
        else:
            test_file = self._root_dir / parent_dir / test_file_name

        test_file.touch()

        return test_file

    def make_dir(self, *, parent_dir: str = None, dirname: str = None) -> Path:
        """テスト用のディレクトリを作成する

        Args:
            parent_dir (str, optional):
                親ディレクトリの指定
                なければ，root_dir 直下に作成される
            dirname (str, optional):
                ディレクトリ名はクラス生成時に指定したディレクトリを root とした
                相対パスで指定する．
                指定がなければ，自動的にディレクトリ名を生成する
                生成されるファイル名 testdir_<作成された回数(0 から)>

        Returns:
            Path: 生成したディレクトリの pathlib オブジェクト
        """
        if dirname is None:
            test_dir_name \
                = "testdir_" + str(self._make_dir_count)
            self._make_dir_count += 1
        else:
            test_dir_name = dirname

        if parent_dir is None:
            test_dir = self._root_dir / test_dir_name
        else:
            test_dir = self._root_dir / parent_dir / test_dir_name

        test_dir.mkdir()

        return test_dir


@pytest.fixture(scope="class")
def make_dir_and_file(tmp_path_factory):
    def _make(dir_name: str) -> Maker:
        test_dir: Path = tmp_path_factory.mktemp(dir_name)
        maker = Maker(test_dir)

        return maker

    return _make
