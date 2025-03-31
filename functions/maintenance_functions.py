#!/usr/bin/env python3

import argparse
import uuid
import shutil
from pathlib import Path


def get_github_user_repo_from_config(config_path: Path):
    """
    .git/config ファイルを読み込み、GitHub 上のユーザー名と
    リポジトリ名を抜き出して返します。
    取得できない場合は (None, None) を返します。
    """
    if not config_path.is_file():
        return None, None

    lines = config_path.read_text(encoding="utf-8").splitlines()
    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith("url ="):
            url = line_strip.split("=", 1)[1].strip()

            # GitHub 以外のURLをスキップ
            if "github.com" not in url:
                return None, None

            # 例: "git@github.com:username/repo.git" -> ":username/repo.git"
            #     "https://github.com/username/repo.git" -> "/username/repo.git"
            parts = url.split("github.com", 1)[-1]
            parts = parts.lstrip("/").lstrip(
                ":"
            )  # ":username/repo.git" 等の先頭記号を除去

            spl = parts.split("/")
            if len(spl) < 2:
                return None, None

            user = spl[0]
            repo_with_dotgit = spl[1]
            # ".git" を取り除く
            if repo_with_dotgit.endswith(".git"):
                repo = repo_with_dotgit[:-4]
            else:
                repo = repo_with_dotgit

            return user, repo
    return None, None


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


def move_temp_files(dry_run: bool):
    parser = argparse.ArgumentParser(
        description='指定ディレクトリ直下の GitHub リポジトリを "<user>/<repo>" ディレクトリ構造に整理するスクリプト。'
    )
    parser.add_argument(
        "target_directory",
        nargs="?",
        default=".",
        help="Git リポジトリが並んでいるディレクトリパス (デフォルト: カレントディレクトリ)。",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="ファイル移動を実行せず、移動予定のパスだけを表示します。",
    )
    args = parser.parse_args()

    base_dir = Path(args.target_directory).resolve()
    if not base_dir.is_dir():
        print(f"指定されたパスはディレクトリではありません: {base_dir}")
        return

    # base_dir 直下のリポジトリを走査
    for item in base_dir.iterdir():
        if not item.is_dir():
            continue  # ディレクトリ以外は無視

        git_dir = item / ".git"
        if not git_dir.is_dir():
            continue  # gitリポジトリでなければ無視

        config_path = git_dir / "config"
        user, repo = get_github_user_repo_from_config(config_path)
        if not user or not repo:
            print(f"[SKIP] {item.name} は GitHubリポジトリ情報を取得できませんでした。")
            continue

        target_dir = base_dir / user / repo
        if target_dir.exists():
            print(f"[SKIP] すでに {target_dir} が存在します: {item.name}")
            continue

        if args.dry_run:
            print(f"[DRY-RUN] {item} -> {target_dir}")
        else:
            target_dir.parent.mkdir(parents=True, exist_ok=True)
            safe_move(item, target_dir)
            print(f"[MOVE] {item} -> {target_dir}")
