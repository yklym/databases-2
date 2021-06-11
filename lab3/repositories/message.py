from db import red
from models.message import MessageState, messages_stats_param, get_message_by_id_param

class MessageRepository:
    @staticmethod
    def get_next_message_id_save():
        next_message_id = red.get('message:id')
        save_next_id = next_message_id if next_message_id is not None else 1
        red.set('message:id', save_next_id)
        red.incr('message:id')
        return save_next_id


    @staticmethod
    def send_message(text, username_from, username_to):
        massage_id = MessageRepository.get_next_message_id_save()
        message_key = f"message:{massage_id}"
        user_key = f"user:{username_from}"
        red.sadd(f'messages-sent-to:{username_to}', massage_id)
        red.hmset(message_key, {
            'id': massage_id,
            'sender-name': username_from,
            'receiver-name': username_to,
            'text': text,
            'status': MessageState.CREATED
        })
        red.hincrby(user_key, 'created-amount', 1)
        red.hincrby(user_key, 'total-amount', 1)
        red.rpush('messages', f"message:{massage_id}")
        red.hmset(message_key, {
            'status': MessageState.IN_QUEUE,
        })
        red.hincrby(user_key, 'created-amount', -1)
        red.hincrby(user_key, 'in-queue-amount', 1)
        red.zincrby('sent-amount', 1, username_from)

    @staticmethod
    def get_user_incoming_messages(username):
        messages = red.smembers(f'messages-sent-to:{username}')
        return messages

    @staticmethod
    def message_to_string(message_id):
        message = MessageRepository.get_message_by_id(message_id)
        print(message)
        result = (
                f"Id: {message['id']} \n" +
                f"From: {message['sender-name']} to {message['receiver-name']}\n" +
                f"Status: {message['status']}\n" +
                f"Text: {message['text']}"
        )
        return result

    @staticmethod
    def get_user_messages_stats(username):
        user_key = f"user:{username}"
        created, in_queue, spam_checking, spam, sent, delivered, total = red.hmget(
            user_key, messages_stats_param
        )

        result_dict = {
            MessageState.CREATED: created,
            MessageState.IN_QUEUE: in_queue,
            MessageState.IN_SPAM_CHECKING: spam_checking,
            MessageState.BLOCKED_BY_SPAM: spam,
            MessageState.SENT: sent,
            MessageState.DELIVERED: delivered,
        }

        return result_dict, total

    @staticmethod
    def get_next_queue_message():
        message_id = red.lpop('messages')
        if message_id is None:
            return None
        return MessageRepository.get_message_by_id(message_id)

    @staticmethod
    def spam_message_check(message):
        message_key = message['id']
        red.hset(message_key, 'status', MessageState.IN_SPAM_CHECKING)
        sender_key = f"user:{message['sender-name']}"

        red.hincrby(sender_key, 'in-queue-amount', -1)
        red.hincrby(sender_key, 'spam-checking-amount', 1)

        spam_checking_result = MessageRepository.is_spam(message)
        red.hincrby(sender_key, 'spam-checking-amount', -1)
        return spam_checking_result

    @staticmethod
    def is_spam(message):
        message_text = message['text']
        if message_text:
            return 'spam' in message_text
        return False

    @staticmethod
    def on_message_spam(message):
        print(f"Found spam message with id: {message['id']} from {message['sender-name']}")
        message_key = message['id']
        sender_key = f"user:{message['sender-name']}"
        red.hset(message_key, 'status', MessageState.BLOCKED_BY_SPAM)
        red.hincrby(sender_key, 'spam-amount', 1)
        red.zincrby('spam-amount', 1, sender_key)
        red.publish('spam', message['sender-name'])

    @staticmethod
    def on_message_not_spam(message):
        print(f"Processed message with id: {message['id']} from \"{message['sender-name']}\". Not spam")
        message_key = message['id']
        sender_key = f"user:{message['sender-name']}"
        red.zincrby('sent-amount', 1, sender_key)
        red.hincrby(sender_key, 'sent-amount', 1)
        red.hset(message_key, 'status', MessageState.SENT)

    @staticmethod
    def get_message_by_id(message_id):
        sender_name, receiver_name, text, status = red.hmget(
            message_id, get_message_by_id_param
        )
        return {
            'id': message_id,
            'sender-name': sender_name,
            'receiver-name': receiver_name,
            'text': text,
            'status': status,
        }
