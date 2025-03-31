#!/usr/bin/env python3

import shutil
import uuid
from pathlib import Path

def safe_move(src: Path, dst: Path):
    """
    src ディレクトリを dst に移動する。
    もし "Cannot move a directory ... into itself" エラーが出た場合は、
    一時ディレクトリにリネームしてから移動することで回避する。
    """
    try:
        shutil.move(str(src), str(dst))  # shutil.move は str パスが必要
    except shutil.Error as e:
        # e.g. "Cannot move a directory '/path/.../src' into itself '/path/.../src/src'"
        print(f"[INFO] {e}")
        print("[INFO] Trying to move via a temporary directory...")

        base_dir = src.parent
        tmp_name = f".tmpmove_{uuid.uuid4().hex}"  # 一時ディレクトリ用の名前
        tmp_path = base_dir / tmp_name

        src.rename(tmp_path)
        shutil.move(str(tmp_path), str(dst))
