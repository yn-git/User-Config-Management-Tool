# -*- coding: utf-8 -*-
import sys

from tinydb import TinyDB, Query

from .path_translator import DBFilter


class ConfigDB:
    """設定ファイルの管理情報を記録するための DB

    Args:
        json_path (str): db 本体となる json ファイルの path
        filter_ (DBFilter):
            DB 保存用に path を変換する
            また，DB から取り出す際に path をもとに戻す

    Attributes:
        db (TinyDB): TinyDB のインスタンス
        filter:
            DB 保存用に path を変換する
            また，DB から取り出す際に path をもとに戻す
    """

    def __init__(self, json_path: str, filter_: DBFilter):
        self._db = TinyDB(json_path)
        self._filter = filter_

    def add(self, path):
        saving_path = str(self._filter.apply_inward(path))

        query = Query()
        # 同じ path があった場合，追加しない
        if not self._db.search(query.path == saving_path):
            add_data = {"path": saving_path}
            self._db.insert(add_data)
        else:
            # TODO: エラーメッセージを丁寧にする
            print(u"既に追加済みの設定ファイルです.", file=sys.stderr)
            sys.exit(1)

    def delete(self, path):
        saved_path = self._filter.apply_inward(path)

        query = Query()
        if self._db.search(query.path == str(saved_path)):
            self._db.remove(query.path == str(saved_path))
        else:
            print(
                u"DB に登録されていない ファイル・ディレクトリが指定されました．",
                file=sys.stderr)
            sys.exit(1)

    def get_managed_config_list(self):
        # TODO: できれば型アノテーションをつけたい
        config_list = (self._filter.apply_outward(x["path"])
                       for x in self._db.all())
        return config_list
