# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from pathlib import Path
from shutil import copy2, copytree, rmtree
import sys


class Locater(metaclass=ABCMeta):
    def locate(self, origin_path: Path, collect_path: Path):
        self._origin_path = origin_path
        self._collect_path = collect_path

        self._body()

    @abstractmethod
    def _body(self):
        raise NotImplementedError()

    def _select(self, check_path: Path):
        if check_path.is_file():
            self._locate_file()
        elif check_path.is_dir():
            self._locate_dir()
        else:
            sys.exit(1)

    @abstractmethod
    def _locate_file(self):
        raise NotImplementedError()

    @abstractmethod
    def _locate_dir(self):
        raise NotImplementedError()


class Collecter(Locater):
    def _body(self):
        self._select(self._origin_path)
        self._origin_path.symlink_to(
            self._collect_path, target_is_directory=True)

    def _locate_file(self):
        copy2(self._origin_path, self._collect_path)
        self._origin_path.unlink()

    def _locate_dir(self):
        copytree(self._origin_path, self._collect_path)
        rmtree(self._origin_path)


class ReLocater(Locater):
    def _body(self):
        # ファイル or ディレクトリが存在しなかったら，
        # シンボリックリンクを貼るだけでいい
        if self._origin_path.exists():
            self._select(self._collect_path)

        self._origin_path.symlink_to(
            self._collect_path, target_is_directory=True
        )

    def _locate_file(self):
        self._origin_path.unlink()

    def _locate_dir(self):
        rmtree(self._origin_path)


class Undo(Locater):
    def _body(self):
        # シンボリックリンクを削除しておく．
        # なくても ok であるため，そのまま進む．
        try:
            self._origin_path.unlink()
        except FileNotFoundError:
            pass
        self._select(self._collect_path)

    def _locate_file(self):
        copy2(self._collect_path, self._origin_path)
        self._collect_path.unlink()

    def _locate_dir(self):
        copytree(self._collect_path, self._origin_path)
        rmtree(self._collect_path)
