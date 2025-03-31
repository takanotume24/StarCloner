#!/usr/bin/env python3

import argparse
from pathlib import Path
from functions.get_github_user_repo_from_config import get_github_user_repo_from_config
from functions.safe_move import safe_move

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
