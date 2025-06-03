from .base import BaseHandler, BaseImageHandler
from .hugo.hugoHandler import HugoHandler
from .instagram.instagramHandler import InstagramHandler
from .facebook.facebookHandler import FacebookHandler  # WIP

__all__ = ['BaseHandler', 'BaseImageHandler', 'HugoHandler', 'InstagramHandler', 'FacebookHandler']