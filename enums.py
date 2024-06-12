from enum import Enum, auto


class MixinEnum(Enum):
    @classmethod
    def choices(cls):
        return [role for role in cls]


class RoleEnum(MixinEnum):
    # USER = 'User'
    ADMIN = 'Admin'
    EDITOR = 'Editor'
    VIEWER = 'Viewer'
    USER = auto()


class FoodEnum(MixinEnum):
    VEGETARIAN = 'Vegetarian'
