from django_redis import get_redis_connection
import redis

from MxOnline.settings import REDIS_MOBILE

# con = get_redis_connection('default')
# con.set("test", "1")
r = redis.Redis(REDIS_MOBILE)
r.delete('18947682087')