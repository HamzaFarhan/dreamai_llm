from imports import *


def connect_to_server(redis_host="127.0.0.1", redis_port=6379):
    try:
        r = redis.StrictRedis(
            host=redis_host, port=redis_port, charset="utf-8", decode_responses=True
        )
    except Exception as e:
        raise Exception(f"Connecting to Redis Server failed with error {e}")
    return r


class KeyValueStore:
    def __init__(self, redis_host="127.0.0.1", redis_port=6379):
        try:
            self.server = connect_to_server(redis_host=redis_host, redis_port=redis_port)
            # self.logger = logger
        except Exception as e:
            raise

    def insert(self, key, value):
        server = self.server
        # ogger.debug(key,value)
        msg.info(key, value, spaced=True)
        server.hmset(key, value)

    def get(self, key):
        server = self.server
        # logger.debug(key)
        try:
            val = server.hgetall(key)
        except Exception as e:
            # logger.error("unable to retrieve value of key {} from Redis: error = {}".format(key,e))
            raise f"Unable to retrieve value of key {key} from Redis: error = {e}"
        return val

    def getall(self):
        return self.server.keys()

    def remove(self, key):
        server = self.server
        # logger.debug('removing key {}'.format(key))
        msg.info("removing key {}".format(key), spaced=True)
        try:
            all_keys = list(server.hgetall(key).keys())
            server.hdel(key, *all_keys)
            # logger.debug('key {} removed'.format(key))
            msg.info("key {} removed".format(key), spaced=True)
        except Exception as e:
            # logger.error("unable to remove key {} from Redis: error = {}".format(key,e))
            raise f"Unable to remove key {key} from Redis: error = {e}"


def gen_random_string(length):
    return str(uuid.uuid4()).replace("-", "")[:length]


def start_task(kv_store):
    if kv_store is not None:
        task_id = gen_random_string(16)
        task = dict(task_id=task_id, status="TASK_STATUS_IN_PROGRESS")
        kv_store.insert(task_id, task)
        return task_id
    else:
        return None


def fail_task(task_id, kv_store, error):
    if task_id is not None and kv_store is not None:
        task = kv_store.get(task_id)
        task["status"] = "TASK_STATUS_FAILED"
        task["error"] = error
        kv_store.insert(task_id, task)


def finish_task(task_id, kv_store, results=None):
    if task_id is not None and kv_store is not None:
        task = kv_store.get(task_id)
        task["status"] = "TASK_STATUS_FINISHED"
        if results is not None:
            task["results"] = json.dumps(results)
        kv_store.insert(task_id, task)
