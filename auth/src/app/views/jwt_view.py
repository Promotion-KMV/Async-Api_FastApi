import redis
from flask import Blueprint, jsonify, request

from app.services.user_service import UserService

from app.services.jwt_service import JWTService
from app.services.login_history_service import LoginHistoryService
from app.utils.utils import check_password
from flask_jwt_extended import jwt_required, current_user

jwt_blueprint = Blueprint('jwt', __name__, url_prefix='/auth/api/v1')

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


@jwt_blueprint.route('/jwt/login/', methods=['POST'])
def login_user():
    """
    Метод авторизации пользователя
    ---
    parameters:
      - in: body
        name: login
        description: login пользователя
        schema:
            type: object
            required:
              - login
              - password
            properties:
              login:
                type: string
                example: login
              password:
                type: string
                example: 123qweQWE!@#
    responses:
      200:
        description: Пользователь успешно авторизован
      401:
        description: Неверные данные для входа
    """
    bad_credential_response = jsonify({"msg": "Bad username or password"}), 401
    login, password = request.json.get('login'), request.json.get('password')

    if not login and password:
        return bad_credential_response

    user = UserService.get_user_by_login(login)
    hashed_password = user.password

    is_authorized = check_password(password, hashed_password)

    if not is_authorized:
        return bad_credential_response

    jwt_service = JWTService(user)
    token_pair = jwt_service.obtain_token_pair()

    login_history = LoginHistoryService(user)
    login_history.create(
        user_agent=str(request.user_agent),
        refresh_token=token_pair.get('refresh_token')
    )

    return jsonify(token_pair)


@jwt_blueprint.route('/jwt/who', methods=['GET'])
def who_am_i():
    return jsonify(
        id=current_user.id
    )


@jwt_blueprint.route('/jwt/logout/', methods=['POST'])
@jwt_required()
def logout_user():
    """
    Метод авторизации пользователя
    ---
    parameters:
      - in: body
    responses:
      200:
        description: Пользователь успешно вышел из системы
    """
    # add refresh token to blacklist
    print(current_user)
