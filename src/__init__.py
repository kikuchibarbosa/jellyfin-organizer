"""
Jellyfin Organizer - Sistema de Organização Automática de Animes

Um sistema completo para organização automática de downloads de animes,
com integração ao qBittorrent e compatibilidade com Jellyfin/Plex.
"""

__version__ = "2.0.0"
__author__ = "Hevertton Kikuchi Barbosa"
__email__ = "kikuchibarbosa@gmail.com"
__license__ = "MIT"

from .auto_organize_anime import extract_anime_info, organize_file
from .monitor_downloads import AnimeMonitor
from .config import *

__all__ = [
    "extract_anime_info",
    "organize_file", 
    "AnimeMonitor",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]