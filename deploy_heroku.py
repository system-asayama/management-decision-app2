#!/usr/bin/env python3
"""
Heroku Build APIを使用してアプリケーションをデプロイするスクリプト
"""
import subprocess
import sys
import json
import time

APP_NAME = "management-decision-making-app"

def run_command(cmd, check=True):
    """コマンドを実行して結果を返す"""
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def main():
    print("=" * 60)
    print(f"Deploying to Heroku app: {APP_NAME}")
    print("=" * 60)
    
    # 1. 現在のコミットハッシュを取得
    result = run_command("git rev-parse HEAD")
    commit_hash = result.stdout.strip()
    print(f"✅ Current commit: {commit_hash[:7]}")
    
    # 2. tarballを作成
    print("\n📦 Creating tarball...")
    tarball_name = f"deploy-{commit_hash[:7]}.tar.gz"
    run_command(f"git archive --format=tar.gz -o /tmp/{tarball_name} HEAD")
    print(f"✅ Tarball created: /tmp/{tarball_name}")
    
    # 3. Heroku Build APIを使用してデプロイ
    print(f"\n🚀 Deploying to Heroku...")
    deploy_cmd = f"""
    curl -X POST https://api.heroku.com/apps/{APP_NAME}/builds \\
      -H "Accept: application/vnd.heroku+json; version=3" \\
      -H "Authorization: Bearer $(heroku auth:token)" \\
      -H "Content-Type: application/json" \\
      -d '{{
        "source_blob": {{
          "url": "https://github.com/system-asayama/management-decision-app2/archive/{commit_hash}.tar.gz",
          "version": "{commit_hash[:7]}"
        }}
      }}'
    """
    
    result = run_command(deploy_cmd, check=False)
    
    if result.returncode == 0:
        try:
            response = json.loads(result.stdout)
            build_id = response.get('id', 'unknown')
            print(f"✅ Build started: {build_id}")
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Commit: {commit_hash[:7]}")
            
            # ビルドの完了を待つ
            print("\n⏳ Waiting for build to complete...")
            time.sleep(10)
            
            # リリース情報を取得
            print("\n📋 Checking release status...")
            run_command(f"heroku releases --app {APP_NAME} --num 1")
            
            print("\n✅ Deployment completed successfully!")
            print(f"🌐 App URL: https://{APP_NAME}.herokuapp.com")
            
        except json.JSONDecodeError:
            print(f"Response: {result.stdout}")
            print(f"Error: {result.stderr}")
    else:
        print(f"❌ Deployment failed")
        print(f"Error: {result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    main()
