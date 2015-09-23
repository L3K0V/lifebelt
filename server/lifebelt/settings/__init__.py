import os

try:
	from .local_settings import *
except ImportError:
	if 'TRAVIS' in os.environ:
		SECRET_KEY = 'secret'

from .common import *
from .email import *
