"""
データベース初期化スクリプト
テーブルを作成し、初期データを投入する
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# 環境変数からデータベースURLを取得
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/management_decision_app')

# エンジン作成
engine = create_engine(DATABASE_URL, echo=True)

# セッション作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    """データベースを初期化"""
    print("データベーステーブルを作成中...")
    Base.metadata.create_all(bind=engine)
    print("✅ データベーステーブルの作成が完了しました")

if __name__ == "__main__":
    init_database()
