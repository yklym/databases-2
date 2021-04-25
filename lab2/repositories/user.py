from db import r
from models.user import create_user_object


class UserRepository:
    @staticmethod
    def register(username):
        user_key = f"user:{username}"
        r.sadd('users', username)
        user_exists = r.exists(user_key)
        if user_exists:
            return
        r.hmset(user_key, create_user_object(username))
        r.publish('login', username)

    @staticmethod
    def logout(username):
        r.publish('logout', username)
        r.srem('users', username)

    @staticmethod
    def get_most_active_senders():
        top_senders_amount = 10
        return r.zrange('sent-amount', 0, top_senders_amount, desc=True, withscores=True)

    @staticmethod
    def get_most_active_spammers():
        top_spammers_amount = 10
        return r.zrange('spam-amount', 0, top_spammers_amount, desc=True, withscores=True)

    @staticmethod
    def get_users_online():
        return r.smembers('users')
