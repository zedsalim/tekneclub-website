from config.env import env

from .base import *

DEBUG = env.bool("DJANGO_DEBUG", default=True)
