class MessageState:
    CREATED = 'CREATED'
    IN_QUEUE = 'IN_QUEUE'
    IN_SPAM_CHECKING = 'IN_SPAM_CHECKING'
    BLOCKED_BY_SPAM = 'BLOCKED_BY_SPAM'
    SENT = 'SENT'
    DELIVERED = 'DELIVERED'


messages_stats_param = [
    'created-amount',
    'in-queue-amount',
    'spam-checking-amount',
    'spam-amount',
    'sent-amount',
    'delivered-amount',
    'total-amount'
]

get_message_by_id_param = [
    'sender-name',
    'receiver-name',
    'text',
    'status'
]
