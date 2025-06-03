from ..base import BaseImageHandler

class FacebookHandler(BaseImageHandler):
    """
    Handler for Facebook posts.
    Inherits from BaseImageHandler.
    """

    def __init__(self, bot):
        super().__init__(bot)
