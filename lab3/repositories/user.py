from db import red, neo
from models.user import create_user_object


class UserRepository:
    @staticmethod
    def register(username):
        user_key = f"user:{username}"
        red.sadd('users', username)
        user_exists = red.exists(user_key)
        if user_exists:
            return
        red.hmset(user_key, create_user_object(username))
        red.publish('login', username)
        neo.register_user(username)

    @staticmethod
    def logout(username):
        red.publish('logout', username)
        red.srem('users', username)

    @staticmethod
    def get_most_active_senders():
        top_senders_amount = 10
        return red.zrange('sent-amount', 0, top_senders_amount, desc=True, withscores=True)

    @staticmethod
    def get_most_active_spammers():
        top_spammers_amount = 10
        return red.zrange('spam-amount', 0, top_spammers_amount, desc=True, withscores=True)

    @staticmethod
    def get_users_online():
        return red.smembers('users')
