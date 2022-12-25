import random

list = [
    'TrueOffMyChest',
    'confession',
    'confessions',
    'TalesFromRetail',
    'talesfromtechsupport',
    'offmychest',
    'AmItheAsshole',
    'pettyrevenge',
    'relationships',
    'relationship_advice',
    'tifu'
]


def getRandomSub():
    return random.choice(list)
