#!/usr/bin/env python
# coding: utf-8

from src.screens.home.home import HomeScreen
from src.constants.constants import (
    DIRECTORY_IMAGE_PLAYER,
    DIRECTORY_CAPTURES,
    DIRECTORY_AUDIO_PLAYER,
    DIRECTORY_LOGS_IMAGE,
)
from pathlib import Path
from database.database import generate_database

if __name__ == "__main__":
    Path(DIRECTORY_IMAGE_PLAYER).mkdir(exist_ok=True)
    Path(DIRECTORY_AUDIO_PLAYER).mkdir(exist_ok=True)
    Path(DIRECTORY_CAPTURES).mkdir(exist_ok=True)
    Path(DIRECTORY_LOGS_IMAGE).mkdir(exist_ok=True)

    generate_database()

    home = HomeScreen()
    home.Show()
