# -*- coding: utf-8 -*-
from .database import ConfigDB
from .locate import Locater
from .path_translator import ConfigPath


# CMT(Config Management Tool)
class CMT:
    def __init__(
            self, db: ConfigDB, collect_dir: str):
        self._db = db
        self._collect_dir = collect_dir

    def add(self, add_target: str, locater: Locater):
        translator = ConfigPath(add_target, self._collect_dir)
        origin_path = translator.origin_path(check_exists=True)
        collect_path = translator.collect_path()

        self._db.add(origin_path)
        # 設定ファイルを管理するディレクトリに，
        # 指定したファイル or ディレクトリをコピーし，
        # そこからシンボリックリンクを元の場所に貼る
        locater.locate(origin_path, collect_path)

    def relocate(self, locater: Locater):
        # db に登録されている設定ファイルのシンボリックリンクを貼り直す
        config_list = self._db.get_managed_config_list()
        for origin_path in config_list:
            translator = ConfigPath(origin_path, self._collect_dir)
            collect_path = translator.collect_path(check_exists=True)
            locater.locate(origin_path, collect_path)

    def delete(self, del_target: str, locater: Locater):
        # HACK:シンボリックリンクが何らかの理由で切られていた場合，
        # 処理が中断してしまう．
        translator = ConfigPath(del_target, self._collect_dir)
        origin_path = translator.origin_path()
        collect_path = translator.collect_path(check_exists=True)

        self._db.delete(origin_path)
        # collectdir にあるファイル・ディレクトリの実体を元の場所にコピーし，
        # collectdir のファイル・ディレクトリを削除する
        locater.locate(origin_path, collect_path)
