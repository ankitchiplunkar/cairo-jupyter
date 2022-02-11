with open("../VERSION", 'r') as f:
    __version__ = f.read()

from .kernel import CairoKernel