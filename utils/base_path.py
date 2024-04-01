from os import getcwd, mkdir
from os.path import join, exists

class BasePath:
    @property
    def BASE():
        BASE = join(getcwd(), 'temp')
        if not exists(BASE):
            mkdir(BASE)

        return BASE