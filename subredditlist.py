import random

list = [
    'TrueOffMyChest',
    'confession',
    'TalesFromRetail',
    'talesfromtechsupport',
    'offmychest',
    'AmItheAsshole',
    'pettyrevenge',
    'relationships',
    'relationship_advice'
]


def getRandomSub():
    return random.choice(list)
