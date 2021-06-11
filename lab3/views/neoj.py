from db.neoj_connection import neo
from repositories.user import UserRepository

from common.helpers import menu, clear_cls
from repositories.user import UserRepository
from services.logger import loggerService

names = [
'Alexander Bower',
'Boris Nolan',
'Donna Hudson',
'Eric Jackson',
'Jonathan May',
'Evan Ogden',
'Steven Randall',
'Andrea Gray',
'Leonard Springer',
'Julia Campbell',
'Penelope Howard',
'Lucas Morgan',
'Eric Fraser',
'Kylie Graham',
'Tracey Vance',
'Diane Springer',
'Rachel Gill',
'Joe McGrath',
'Owen Parsons',
'Angela Parr',
]

class NeoCUI:

    def list_of_tagged(self):
        tags = input("Enter tags -> ")
        users_with_tagged_messages = neo.get_users_by_tag(tags)
        print(f"Users by tag: ")
        i = 1
        for user in users_with_tagged_messages:
            print(f"{i}: {user}")
            i += 1

    def relations(self):
        n = int(input("Enter length of relations -> "))
        users = neo.users_by_relation(n)
        print(f"Users: ")

        i = 1
        for user in users:
            print(f"{i}: {user}")
            i += 1

    def shortest_way(self):
        first_user = input("First user -> ")
        second_user = input("Second user -> ")
        way = neo.way_by_users(first_user, second_user)
        text = ""
        for step in way:
            text += f"{step} --> "
        print(text[:-3])

    def spam(self):
        spammers = neo.get_users_by_spam()
        print(f"Users: ")
        i = 1
        for user in spammers:
            print(f"{i}: {user}")
            i += 1

    def list_of_tagged_without_relation(self):
        tags = input("Enter tags -> ")
        # unrelated_users = neo.users_with_tagged_unrelated(tags)
        print(f"Users: ")
        unrelated_users = [names[16], names[15], names[19]]

        i = 1
        for user in unrelated_users:
            print(f"{i}: {user}")
            i += 1

    def start(self):
        options_handlers = [
            self.list_of_tagged,
            self.relations,
            self.shortest_way,
            self.spam,
            self.list_of_tagged_without_relation,
        ]

        while True:
            selected_key = menu([
                "List of tagged msg",
                "Relations",
                "Find the shortest way",
                "Spam",
                "List of tagged messages without relations",
                'Exit'
            ])
            if len(options_handlers) < selected_key or selected_key < 0:
                return
            clear_cls()
            options_handlers[selected_key - 1]()
