from app.core import db

from app.models.db_models import LoginHistory as DBLoginHistory
from app.models.db_models import User as DBUserModel


class LoginHistoryService:
    user: DBUserModel = None

    def __init__(self, user: DBUserModel):
        self.user = user

    def create(self, user_agent: str, refresh_token: str) -> DBLoginHistory:
        """
        Добавление истории успешной авторизации для пользователя
        """
        entry = DBLoginHistory(user_agent=user_agent, refresh_token=refresh_token)
        self.user.history_entries.append(entry)
        db.session.commit()
        return entry

    def list(self):
        """
        Просмотр истории авторизации пользователя
        """
        entries = self.user.history_entries
        return entries
