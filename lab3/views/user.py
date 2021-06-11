from common.helpers import menu, clear_cls
from repositories.message import MessageRepository
from repositories.user import UserRepository


class UserCUI:

    def __init__(self):
        self.username = None

    def send_message(self):
        receiver_name = input("Enter receiver name: ")
        message = input("Enter message: ")
        MessageRepository.send_message(message, self.username, receiver_name)

    def inbox(self):
        print('\n\n'.join([MessageRepository.message_to_string(f"{message}") for message in
                           MessageRepository.get_user_incoming_messages(self.username)]))

    def start(self):
        selectied_key = menu(["Login", "Exit"])
        if selectied_key == 1:
            name = input("Enter name: ")
            self.username = name
            UserRepository.register(name)
            self.main_menu()

    def main_menu(self):
        selected_key = 1
        options_handlers = [
            self.send_message,
            self.inbox,
            self.own_messages_stats,
            self.logout
        ]
        while True:
            selected_key = menu([
                "Send message",
                "Inbox",
                "Statistics",
                "Logout"
            ])
            if len(options_handlers) < selected_key or selected_key < 0:
                return
            clear_cls()
            options_handlers[selected_key - 1]()

    def own_messages_stats(self):
        message_states, total_count = MessageRepository.get_user_messages_stats(self.username)
        print(message_states, f'Total sent: {total_count}')

    def logout(self):
        UserRepository.logout(self.username)
        self.username = None
        self.start()
