from services.logger import loggerService
from repositories.user import UserRepository
from common.helpers import menu, clear_cls


class AdminCUI:

    def most_active_senders(self):
        senders = UserRepository.get_most_active_senders()
        print(f"Senders in list: {len(users)}")
        print('\n'.join([f"{user} - {count}" for (user, count) in senders]))

    def most_active_spammers(self):
        spammers = UserRepository.get_most_active_spammers()
        print(f"Spammers in list: {len(users)}")
        print('\n'.join([f"{user} - {count}" for (user, count) in spammers]))


    def start(self):
        selected_key = 1

        options_handlers = [
            lambda _: print(loggerService.get_logs()),
            self.users_online,
            self.most_active_senders,
            self.most_active_spammers,
        ]

        while len(options_handlers) + 1 > selected_key > 0:
            selected_key = menu([
                "Logs",
                "Users online",
                "Most active senders",
                "Most active spammers",
                "Exit"
            ])
            clear_cls()
            options_handlers[selected_key - 1]()

    def users_online(self):
        users = UserRepository.get_users_online()
        print(f"Users online {len(users)}")
        print('\n'.join(users))



