"""
認証用のBlueprint
ログイン、ログアウト、ユーザー情報取得のエンドポイントを提供
"""
from __future__ import annotations
from flask import Blueprint, request, jsonify, make_response, session
from app.auth import auth_service

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/me', methods=['GET'])
def get_current_user():
    """
    現在ログイン中のユーザー情報を取得
    
    Returns:
        JSON: ユーザー情報またはnull
    """
    user = auth_service.authenticate_request(request)
    
    if user:
        return jsonify({
            'id': user.id,
            'openId': user.open_id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'createdAt': user.created_at.isoformat(),
            'updatedAt': user.updated_at.isoformat()
        })
    else:
        return jsonify(None), 200


@bp.route('/login', methods=['POST'])
def login():
    """
    ログイン処理
    
    Request Body:
        {
            "username": "string",
            "password": "string"
        }
    
    Returns:
        JSON: ログイン成功時はユーザー情報とトークン、失敗時はエラーメッセージ
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # TODO: データベースでユーザー認証
    # 現在はモック実装
    if username and password:
        # モックユーザーを返す
        user = auth_service.get_mock_user()
        
        # セッショントークンを生成
        token = auth_service.create_session_token(user)
        
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
        
        # レスポンスにCookieを設定
        response = make_response(jsonify({
            'user': {
                'id': user.id,
                'openId': user.open_id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            },
            'token': token
        }))
        
        # HTTPOnly Cookieにトークンを設定
        response.set_cookie(
            'session_token',
            token,
            max_age=365*24*60*60,  # 1年
            httponly=True,
            secure=False,  # 本番環境ではTrueに設定
            samesite='Lax'
        )
        
        return response
    else:
        return jsonify({'error': 'Username and password are required'}), 400


@bp.route('/logout', methods=['POST'])
def logout():
    """
    ログアウト処理
    
    Returns:
        JSON: 成功メッセージ
    """
    auth_service.logout()
    
    response = make_response(jsonify({'message': 'Logged out successfully'}))
    
    # Cookieを削除
    response.set_cookie('session_token', '', max_age=0)
    
    return response


@bp.route('/oauth/callback', methods=['GET'])
def oauth_callback():
    """
    OAuth認証のコールバックエンドポイント
    
    Query Parameters:
        code: 認証コード
        state: 状態パラメータ
    
    Returns:
        Redirect: ホームページへリダイレクト
    """
    # モック認証が有効な場合はスキップ
    if auth_service.enable_mock_auth:
        return jsonify({'message': 'Mock authentication enabled, OAuth callback skipped'}), 200
    
    code = request.args.get('code')
    state = request.args.get('state')
    
    if not code or not state:
        return jsonify({'error': 'code and state are required'}), 400
    
    # TODO: OAuth認証フローを実装
    # 1. codeをアクセストークンに交換
    # 2. アクセストークンでユーザー情報を取得
    # 3. データベースにユーザーを登録/更新
    # 4. セッショントークンを生成してCookieに設定
    # 5. ホームページにリダイレクト
    
    return jsonify({'message': 'OAuth callback not implemented yet'}), 501
