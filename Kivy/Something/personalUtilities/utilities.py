import os
from pathlib import Path


class Costants:
    windows = ['Login', 'Panel', 'Info']


class Process:
    @staticmethod
    def create_kv():
        for v in Costants.windows:
            if not os.path.exists(f'windows/{v}.kv'):
                Path(f'windows/{v}.kv').touch()

