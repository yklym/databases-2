from common.helpers import menu, clear_cls
from repositories.user import UserRepository
from services.logger import loggerService


class AdminCUI:

    def most_active_senders(self):
        senders = UserRepository.get_most_active_senders()
        print(f"Senders in list: {len(senders)}")
        print('\n'.join([f"{user} - {count}" for (user, count) in senders]))

    def most_active_spammers(self):
        spammers = UserRepository.get_most_active_spammers()
        print(f"Spammers in list: {len(spammers)}")
        print('\n'.join([f"{user} - {count}" for (user, count) in spammers]))

    def logs(self):
        print(logger.get_logs())

    def start(self):
        selected_key = 1

        options_handlers = [
            lambda: print(loggerService.get_logs()),
            self.users_online,
            self.most_active_senders,
            self.most_active_spammers,
        ]

        while True:
            selected_key = menu([
                "Logs",
                "Users online",
                "Most active senders",
                "Most active spammers",
                "Exit"
            ])
            if len(options_handlers) < selected_key or selected_key < 0:
                return
            clear_cls()
            options_handlers[selected_key - 1]()

    def users_online(self):
        users = UserRepository.get_users_online()
        print(f"Users online {len(users)}")
        print('\n'.join(users))
