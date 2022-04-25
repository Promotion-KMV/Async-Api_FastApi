from typing import Dict

from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.db_models import User as DBUserModel


class JWTService:
    user = None
    access_token = None
    refresh_token = None

    def __init__(self, user: DBUserModel) -> None:
        self.user = user

    def obtain_token_pair(self) -> Dict:
        self.access_token = create_access_token(identity=self.user.id)
        self.refresh_token = create_refresh_token(identity=self.user.id)

        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token
        }
