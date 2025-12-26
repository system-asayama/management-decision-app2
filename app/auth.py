"""
認証システムモジュール
management-decision-making-appの認証ロジックをPythonに移植
"""
from __future__ import annotations
import os
from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass
from flask import Request, session
import jwt


@dataclass
class User:
    """ユーザー情報"""
    id: int
    open_id: str
    name: str
    email: Optional[str]
    role: str  # 'admin' or 'user'
    created_at: datetime
    updated_at: datetime


class AuthService:
    """認証サービス"""
    
    def __init__(self):
        self.jwt_secret = os.getenv('JWT_SECRET', 'local-dev-secret-key')
        self.enable_mock_auth = os.getenv('ENABLE_MOCK_AUTH', 'false').lower() == 'true'
        self.is_production = os.getenv('ENV', 'dev') == 'production'
    
    def get_mock_user(self) -> User:
        """モック認証用の固定ユーザーを返す"""
        return User(
            id=1,
            open_id=os.getenv('OWNER_OPEN_ID', 'local-dev-user'),
            name=os.getenv('OWNER_NAME', 'Local Developer'),
            email='dev@localhost',
            role='admin',
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    def authenticate_request(self, request: Request) -> Optional[User]:
        """
        リクエストから認証情報を取得してユーザーを返す
        
        Args:
            request: Flaskのリクエストオブジェクト
            
        Returns:
            認証成功時はUserオブジェクト、失敗時はNone
        """
        # ローカル開発環境でモック認証が有効な場合
        if not self.is_production and self.enable_mock_auth:
            return self.get_mock_user()
        
        # セッションからユーザー情報を取得
        user_data = session.get('user')
        if user_data:
            return User(
                id=user_data['id'],
                open_id=user_data['open_id'],
                name=user_data['name'],
                email=user_data.get('email'),
                role=user_data.get('role', 'user'),
                created_at=datetime.fromisoformat(user_data['created_at']),
                updated_at=datetime.fromisoformat(user_data['updated_at'])
            )
        
        # Cookieからセッショントークンを取得
        token = request.cookies.get('session_token')
        if token:
            try:
                user = self.verify_session_token(token)
                if user:
                    # セッションに保存
                    session['user'] = {
                        'id': user.id,
                        'open_id': user.open_id,
                        'name': user.name,
                        'email': user.email,
                        'role': user.role,
                        'created_at': user.created_at.isoformat(),
                        'updated_at': user.updated_at.isoformat()
                    }
                    return user
            except Exception as e:
                print(f"[Auth] Token verification failed: {e}")
        
        return None
    
    def create_session_token(self, user: User, expires_in_days: int = 365) -> str:
        """
        ユーザーのセッショントークンを生成
        
        Args:
            user: ユーザーオブジェクト
            expires_in_days: トークンの有効期限（日数）
            
        Returns:
            JWTトークン文字列
        """
        payload = {
            'open_id': user.open_id,
            'name': user.name,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(days=expires_in_days)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def verify_session_token(self, token: str) -> Optional[User]:
        """
        セッショントークンを検証してユーザー情報を返す
        
        Args:
            token: JWTトークン文字列
            
        Returns:
            検証成功時はUserオブジェクト、失敗時はNone
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            
            # TODO: データベースからユーザー情報を取得
            # 現在はトークンの情報のみから復元
            return User(
                id=1,  # TODO: DBから取得
                open_id=payload['open_id'],
                name=payload['name'],
                email=None,  # TODO: DBから取得
                role=payload.get('role', 'user'),
                created_at=datetime.now(),  # TODO: DBから取得
                updated_at=datetime.now()   # TODO: DBから取得
            )
        except jwt.ExpiredSignatureError:
            print("[Auth] Token expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"[Auth] Invalid token: {e}")
            return None
    
    def logout(self):
        """ログアウト処理（セッションをクリア）"""
        session.clear()


# グローバルインスタンス
auth_service = AuthService()
