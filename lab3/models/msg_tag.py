from enum import Enum

class Tag(Enum):
    cats = 1,
    puppies = 2,
    kitties = 3
    doggies = 4,
    rabbits = 5,
    guinea_pigs = 6,
    rats = 7,
    turtles = 8,

    @classmethod
    def has_member(cls, data):
        return data in Tag._member_names_