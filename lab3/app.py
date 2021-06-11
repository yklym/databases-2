from views.admin import AdminCUI
from views.user import UserCUI
from views.neoj import NeoCUI
from services.seeder import run_seed
from services.subscription_listener import MessagesListener
from common.helpers import menu

user_cui = UserCUI()
admin_cui = AdminCUI()
neo_cui = NeoCUI()

def main():
    subs_listener = MessagesListener()
    subs_listener.setDaemon(True)
    subs_listener.start()

    selected_key = 1
    options_handlers = [
        user_cui.start,
        admin_cui.start,
        run_seed,
        neo_cui.start
    ]

    while 0 < selected_key < len(options_handlers) + 1:
        selected_key = menu([
            'user',
            'admin',
            'generate data',
            'neoj4'
        ])

        options_handlers[selected_key - 1]()


if __name__ == '__main__':
    main()
