# handlers/__init__.py

from .commands import register_command_handlers
from .callbacks import register_callback_handlers

def register_handlers(app):
    register_command_handlers(app)
    register_callback_handlers(app)
