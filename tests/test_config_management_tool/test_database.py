# -*- coding: utf-8 -*-
import pytest

from src.ucmt.database import ConfigDB
from src.ucmt.path_translator import DBFilter


@pytest.fixture(scope="class")
def test_db(make_dir_and_file):
    maker = make_dir_and_file("test_db")
    json_db_name = maker.make_file(filename="db.json")

    db = ConfigDB(json_db_name, DBFilter(maker.root_dir))
    return db, maker


class TestConfigDB:
    def test_from_add_to_getlist(self, test_db):
        db, maker = test_db
        file_ = maker.make_file()

        # 1回目は成功する
        assert db.add(file_) is None

        # 重複するため，2回目は失敗する
        with pytest.raises(SystemExit):
            db.add(file_)

        # add した結果を利用する
        list_ = db.get_managed_config_list()
        for config_path in list_:
            assert file_ == config_path
