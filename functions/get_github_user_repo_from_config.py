#!/usr/bin/env python3

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
