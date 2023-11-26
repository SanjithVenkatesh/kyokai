"""
A utility module to represent the origin of a Rikishi
"""
from constants import *

class Shusshin:

    def __init__(self, *args):
        self.country = JAPAN
        if len(args) == 2:
            pass