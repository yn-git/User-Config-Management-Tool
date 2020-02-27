# -*- coding: utf-8 -*-
from pathlib import Path
import pytest

from src.ucmt.cmt import CMT
from src.ucmt.database import ConfigDB
from src.ucmt.path_translator import DBFilter
from src.ucmt.locate import Collecter, ReLocater,\
    Undo


@pytest.fixture(scope="function")
def test_adder(make_dir_and_file):
    maker = make_dir_and_file("test_add")
    db_path = maker.make_file(filename="db.json")
    collect_dir = maker.make_dir()

    filter_ = DBFilter(maker.root_dir)
    db = ConfigDB(str(db_path), filter_)

    adder = CMT(db, str(collect_dir))

    return adder, collect_dir, maker


class TestAdd():
    locater = Collecter()

    def test_normal(self, test_adder):
        adder, collect_dir, maker = test_adder
        test_file = maker.make_file()
        test_dir = maker.make_dir()

        adder.add(str(test_file), self.locater)
        adder.add(str(test_dir), self.locater)

        collect_file = collect_dir / test_file.name
        # ファイルの場合
        assert collect_file.exists() is True
        assert test_file.is_symlink() is True

        collect_dir = collect_dir / test_dir.name
        # ディレクトリの場合
        assert collect_dir.exists() is True
        assert test_dir.is_symlink() is True

    def test_not_exist(self, test_adder):
        adder, _, _ = test_adder
        with pytest.raises(SystemExit):
            adder.add("non_exist", self.locater)

    def test_not_in_rootdir(self, test_adder):
        adder, _, maker = test_adder
        root_dir = Path(maker.root_dir)
        no_in_rootdir = root_dir.parent / "no_in_rootdir"
        no_in_rootdir.touch()

        with pytest.raises(SystemExit):
            adder.add(str(no_in_rootdir), self.locater)


@pytest.fixture(scope="function")
def cmt_setup(make_dir_and_file):
    maker = make_dir_and_file("test_cmt")

    collect_dir = maker.make_dir(dirname="collect-dir")
    db_path = maker.make_file(filename="db.json")
    filter_ = DBFilter(maker.root_dir)
    db = ConfigDB(str(db_path), filter_)
    cmt = CMT(db, str(collect_dir))

    return maker, db, cmt, collect_dir


class TestRelocate:
    locater = ReLocater()

    def test_no_remove(self, cmt_setup):
        maker, db, cmt, collect_dir = cmt_setup

        test_file = maker.make_file(parent_dir=collect_dir.name)
        test_dir = maker.make_file(parent_dir=collect_dir.name)

        # 設定ファイル・ディレクトリが一つ登録済みの db を準備
        # rootdir/test_file・dir が元々設定ファイルがあった path と仮定
        db._db.insert({"path": test_file.name})
        db._db.insert({"path": test_dir.name})

        cmt.relocate(self.locater)

        assert Path(maker.root_dir + "/" + test_file.name).is_symlink() is True
        assert Path(maker.root_dir + "/" + test_dir.name).is_symlink() is True

    def test_with_remove(self, cmt_setup):
        maker, db, cmt, collect_dir = cmt_setup

        # シンボリック先に削除対象の同名ファイルを作っておく
        test_file = maker.make_file(parent_dir=collect_dir.name)
        origin_file = Path(maker.root_dir + "/" + test_file.name)
        test_dir = maker.make_file(parent_dir=collect_dir.name)
        origin_dir = Path(maker.root_dir + "/" + test_dir.name)

        # 設定ファイル・ディレクトリを db にセットしておく
        # rootdir/test_file が元々設定ファイルがあった path と仮定
        db._db.insert({"path": test_file.name})
        db._db.insert({"path": test_dir.name})

        cmt = CMT(db, str(collect_dir))
        cmt.relocate(self.locater)

        assert origin_file.is_symlink() is True
        assert origin_dir.is_symlink() is True

    def test_no_in_collectdir(self, cmt_setup):
        _, db, cmt, _ = cmt_setup
        # collect_dir にないファイルを挿入
        db._db.insert({"path": "no_exists"})

        with pytest.raises(SystemExit):
            cmt.relocate(self.locater)


class TestDelete:
    def test_normal(self, cmt_setup):
        locater = Undo()
        maker, db, cmt, collect_dir = cmt_setup

        test_file = maker.make_file(parent_dir=collect_dir)
        test_dir = maker.make_dir(parent_dir=collect_dir)
        link_test_file = Path(maker.root_dir + "/" + test_file.name)
        link_test_file.symlink_to(test_file)
        link_test_dir = Path(maker.root_dir + "/" + test_dir.name)
        link_test_dir.symlink_to(test_dir)

        db._db.insert({"path": test_file.name})
        db._db.insert({"path": test_dir.name})
        cmt.delete(str(link_test_file), locater)
        cmt.delete(str(link_test_dir), locater)

        assert link_test_file.is_file() is True
        assert test_file.exists() is False

        assert link_test_dir.is_dir() is True
        assert test_dir.exists() is False
