import redis

from app.core.config import RedisConfig

settings = RedisConfig()

redis_ref_tokens = redis.Redis(db=1, **settings.dict())
redis_revoked_tokens = redis.Redis(db=2, **settings.dict())
redis_log_out_all = redis.Redis(db=3, **settings.dict())
redis_upd_roles = redis.Redis(db=4, **settings.dict())
redis_rate_limits = redis.Redis(db=5, **settings.dict())
redis = redis.Redis(**settings.dict())

def get_redis():
    return redis
