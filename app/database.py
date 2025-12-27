"""
データベース接続とセッション管理
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

# 環境変数からデータベースURLを取得
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/management_decision_app')

# エンジン作成
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 接続の健全性チェック
    pool_recycle=3600,   # 1時間ごとに接続をリサイクル
    echo=False           # SQLログを出力しない（本番環境）
)

# セッションファクトリー
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# スレッドセーフなセッション
db_session = scoped_session(SessionLocal)


@contextmanager
def get_db():
    """
    データベースセッションを取得するコンテキストマネージャー
    
    使用例:
        with get_db() as db:
            companies = db.query(Company).all()
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db_session():
    """
    Flask依存性注入用のデータベースセッション取得関数
    
    使用例（Flask Blueprint内）:
        db = get_db_session()
        try:
            companies = db.query(Company).all()
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
    """
    return SessionLocal()
