#!/usr/bin/env python3
"""
Heroku Build APIを使用してデプロイするスクリプト
"""

import os
import requests
import subprocess
import time

# Heroku設定
HEROKU_APP_NAME = "management-decision-making-app"
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")

if not HEROKU_API_KEY:
    print("エラー: HEROKU_API_KEY環境変数が設定されていません")
    exit(1)

# GitHubリポジトリ情報を取得
try:
    repo_url = subprocess.check_output(
        ["git", "config", "--get", "remote.origin.url"],
        cwd="/home/ubuntu/management-decision-app2"
    ).decode().strip()
    
    # GitHubリポジトリURLからowner/repoを抽出
    if "github.com" in repo_url:
        if repo_url.endswith(".git"):
            repo_url = repo_url[:-4]
        repo_path = repo_url.split("github.com/")[-1]
        print(f"GitHubリポジトリ: {repo_path}")
    else:
        print("エラー: GitHubリポジトリではありません")
        exit(1)
    
    # 現在のコミットハッシュを取得
    commit_hash = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd="/home/ubuntu/management-decision-app2"
    ).decode().strip()
    print(f"コミットハッシュ: {commit_hash}")
    
except Exception as e:
    print(f"エラー: Gitリポジトリ情報の取得に失敗しました: {e}")
    exit(1)

# Heroku Build APIを使用してデプロイ
print(f"\n{HEROKU_APP_NAME}にデプロイを開始します...")

headers = {
    "Accept": "application/vnd.heroku+json; version=3",
    "Authorization": f"Bearer {HEROKU_API_KEY}",
    "Content-Type": "application/json"
}

# ビルドを作成
build_data = {
    "source_blob": {
        "url": f"https://github.com/{repo_path}/tarball/{commit_hash}",
        "version": commit_hash[:7]
    }
}

response = requests.post(
    f"https://api.heroku.com/apps/{HEROKU_APP_NAME}/builds",
    headers=headers,
    json=build_data
)

if response.status_code == 201:
    build = response.json()
    build_id = build["id"]
    print(f"✓ ビルドを作成しました (ID: {build_id})")
    print(f"ステータス: {build['status']}")
    
    # ビルドの完了を待つ
    print("\nビルドの進行状況を監視しています...")
    max_wait = 300  # 最大5分待つ
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        response = requests.get(
            f"https://api.heroku.com/apps/{HEROKU_APP_NAME}/builds/{build_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            build_status = response.json()
            status = build_status["status"]
            print(f"ステータス: {status}")
            
            if status == "succeeded":
                print("\n✓ デプロイが成功しました！")
                print(f"アプリURL: https://{HEROKU_APP_NAME}-389a62508f9a.herokuapp.com")
                break
            elif status == "failed":
                print("\n✗ デプロイが失敗しました")
                exit(1)
        
        time.sleep(10)
    
else:
    print(f"✗ ビルドの作成に失敗しました: {response.status_code}")
    print(response.text)
    exit(1)
