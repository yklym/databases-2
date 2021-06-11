def create_user_object(username):
    return {
        'username': username,
        'created-count': 0,
        'in-queue-count': 0,
        'spam-checking-count': 0,
        'spam-count': 0,
        'sent-amount': 0,
        'delivered-count': 0,
        'total-count': 0,
    }