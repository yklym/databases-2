from common.helpers import menu
from views.admin import AdminCUI
from views.user import UserCUI
from services.seeder import seederService

user_cui = UserCUI()
admin_cui = AdminCUI()


def main():
    selected_key = 1
    options_handlers = [
        user_cui.start,
        admin_cui.start,
        seederService.seed_mocks
    ]

    while 0 < selected_key < len(options_handlers) + 1:
        selected_key = menu([
            'user',
            'admin',
            'generate data'
        ])
        options_handlers[selected_key - 1]()


if __name__ == '__main__':
    main()
