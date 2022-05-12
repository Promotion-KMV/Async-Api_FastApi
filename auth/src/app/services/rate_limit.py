import time
from math import floor
from typing import Optional

from flask import request
from pydantic import BaseModel

from app.core.config import Config
from app.db.redis import redis_rate_limits
from app.utils.exceptions import RequestLimitReached
from app.utils.logger import logger
from redis.exceptions import WatchError
from redis.client import Pipeline

config = Config()


class TokenBucketInfo(BaseModel):
    tokens: int
    last_time_stamp: float


class TokenBucket:
    def __init__(
        self,
        rpm: int,
        session_length_sec: int = config.RATE_LIMIT_SESSION_LEN
    ):
        self.rpm = rpm
        self.storage = redis_rate_limits
        self.session_len = session_length_sec

    def pop_token(self, key: str) -> bool:
        """cover rate limiting with redis-trnsaction logic"""
        with self.storage.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(key)
                    return self._pop_token(key, pipe)
                except WatchError:
                    continue
    
    def _pop_token(self, key: str, pipe: Pipeline):
        """logic for token processing"""
        token_info = self._get_from_storage(key, pipe)

        if token_info is None:
            token_info = self._create_session(key, pipe)
            
        if token_info.tokens < 1:
            has_tokens = self._check_and_refill(key, pipe)
            if has_tokens < 1:
                out = False
            else:
                out = True
        else:
            pipe.multi()
            token_info.tokens = token_info.tokens - 1
            pipe.setex(key, self.session_len, token_info.json())
            out = True
        pipe.execute()
        logger.info(token_info)
        return out

    def _create_session(self, key: str, pipe: Pipeline) -> TokenBucketInfo:
        to_storage = TokenBucketInfo(
            tokens=self.rpm,
            last_time_stamp=time.time(),
        )
        pipe.setex(key, self.session_len, to_storage.json())

        return to_storage

    def _check_and_refill(self, key, pipe: Pipeline) -> int:
        token_info = self._get_from_storage(key, pipe)
        if token_info is None:
            return 0
        last_token_upd = token_info.last_time_stamp
        sec_passed = time.time() - last_token_upd
        new_tokens = min(
            floor(sec_passed / 60 * self.rpm),
            self.rpm
        )
        if new_tokens > 0:
            token_info.tokens = new_tokens
            pipe.setex(key, self.session_len, token_info.json())
        return new_tokens

    def _get_from_storage(self, key: str, pipe: Pipeline) -> Optional[TokenBucketInfo]:
        token_info = pipe.get(key)
        out = None
        if token_info is not None:
            out = TokenBucketInfo.parse_raw(token_info)
        return out


token_bucket = TokenBucket(rpm=config.RATE_LIMIT)


def check_rate_limit(key: str):

    if not token_bucket.pop_token(key=key):
        raise RequestLimitReached


def limit_rate(func):
    def wrapper(*args, **kwargs):
        ip_address = request.remote_addr
        check_rate_limit(key=ip_address)
        return func(*args, **kwargs)
    return wrapper

