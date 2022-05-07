import os
from urllib.parse import urlencode
from http import HTTPStatus

import requests
from flasgger import swag_from
from flask import Blueprint, request
from flask.views import MethodView

from app.core.swagger_config import SWAGGER_DOCS_PATH
from app.services.oauth_service import oauth_service
from app.views.utils.decorator import catch_exceptions

oauth_blueprint = Blueprint('oauth', __name__, url_prefix='/auth/api/v1/oauth')

VK_CLIENT_ID = 8158992
VK_CLIENT_SECRET = os.getenv("VK_CLIENT_SECRET")
VK_BASE_URL = "https://oauth.vk.com"
VK_AUTH_URL = VK_BASE_URL + "/authorize"
VK_GET_TOKEN_URL = VK_BASE_URL + "/access_token"
VK_REDIRECT_URI = "http://localhost/auth/api/v1/oauth/vk/login"
VK_API_URL = "https://api.vk.com/method/"
VK_API_VERSION = "5.131"


class OauthView(MethodView):
    @swag_from(
        f"{SWAGGER_DOCS_PATH}/oauth/vk.yaml",
        endpoint="oauth.vk_auth",
        methods=["GET"]
    )
    @catch_exceptions
    def get(self):
        params = {
            "client_id": VK_CLIENT_ID,
            "redirect_uri": VK_REDIRECT_URI,
            "display": "page",
            "response_type": "code"
        }
        vk_url_params = urlencode(params)
        url = f"{VK_AUTH_URL}?{vk_url_params}"

        return {"url": url}, 200


class OauthLoginView(MethodView):
    @swag_from(
        f"{SWAGGER_DOCS_PATH}/oauth/login.yaml",
        endpoint="oauth.vk_login",
        methods=["GET"]
    )
    @catch_exceptions
    def get(self):
        code = request.args["code"]
        get_token_params = {
            "client_id": VK_CLIENT_ID,
            "client_secret": VK_CLIENT_SECRET,
            "redirect_uri": VK_REDIRECT_URI,
            "code": code,
        }
        get_token_response = requests.get(VK_GET_TOKEN_URL, params=get_token_params)

        if get_token_response.status_code == HTTPStatus.OK:
            vk_user_data = get_token_response.json()
            user_id = vk_user_data["user_id"]

            access_token, refresh_token = oauth_service.process_oauth(
                str(user_id),
                "VK",
                request.headers.get("USER_AGENT")
            )

            return {"access_token": access_token, "refresh_token": refresh_token}, HTTPStatus.OK
        else:
            return get_token_response.text, get_token_response.status_code


oauth_blueprint.add_url_rule(
    '/vk/login/',
    endpoint='vk_login',
    view_func=OauthLoginView.as_view('auth'),
    methods=["GET"]
)
oauth_blueprint.add_url_rule(
    '/vk/auth/',
    endpoint='vk_auth',
    view_func=OauthView.as_view('auth'),
    methods=["GET"]
)