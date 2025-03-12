# Copyright (c) 2025 Linh Pham
# marsupialgurgle-audio-parsing is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Marsupial Gurgle Audio File Parsing Tool."""

import json
import sys
from pathlib import Path
from typing import Any

from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import MySQLCursor
from tinytag import TinyTag, TinyTagException


class TagMetadata:  # pylint: disable=too-few-public-methods
    """Audio clip tag metadata."""

    title: str
    album: str
    artist: str
    year: int


class ClipInformation:  # pylint: disable=too-few-public-methods
    """Audio clip information."""

    key: str
    parent: str
    stem: str
    suffixes: list[str]
    tag_metadata: TagMetadata


def parse_audio_tags(audio_file_path: str) -> dict[str, int | str] | None:
    """Parse audio file tags."""
    try:
        _file_tags: TinyTag = TinyTag.get(audio_file_path)

        if _file_tags:
            return {
                "album": _file_tags.album,
                "artist": _file_tags.artist,
                "title": _file_tags.title,
                "year": _file_tags.year,
            }
        else:
            return None
    except TinyTagException:
        return None


def create_database_entries(
    clips_info: dict[str, str | int], database_settings: dict[str, Path | str | int | bool]
) -> None:
    """Create database entries for all available clips."""
    if not database_settings:
        return None

    _database_connection: MySQLConnection = connect(**database_settings)
    for clip in clips_info:
        clip_info = clips_info[clip]
        has_mp3: bool = ".mp3" in clip_info["suffixes"]
        has_m4a: bool = ".m4a" in clip_info["suffixes"]
        has_m4r: bool = ".m4r" in clip_info["suffixes"]
        _cursor: MySQLCursor = _database_connection.cursor()
        query = (
            "INSERT INTO `clips` (`key`, `stem`, `parent`, `mp3`, `m4a`, `m4r`) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        _cursor.execute(
            query,
            (
                clip_info["key"],
                clip_info["stem"],
                clip_info["parent"],
                has_mp3,
                has_m4a,
                has_m4r,
            ),
        )
        _cursor.close()

        if "tags" in clip_info and clip_info["tags"]:
            _cursor = _database_connection.cursor()
            query = "SELECT `id` FROM `clips` WHERE `key` = %s LIMIT 1"
            _cursor.execute(query, (clip_info["key"],))
            result = _cursor.fetchone()
            _cursor.close()

            if result:
                _id = result[0]

                _cursor = _database_connection.cursor()
                query = (
                    "INSERT INTO `tags` (`clip_id`, `artist`, `album`, `title`, `year`) "
                    "VALUES (%s, %s, %s, %s, %s)"
                )
                _cursor.execute(
                    query,
                    (
                        _id,
                        clip_info["tags"].get("artist"),
                        clip_info["tags"].get("album"),
                        clip_info["tags"].get("title"),
                        clip_info["tags"].get("year"),
                    ),
                )
                _cursor.close()
        else:
            print(f"{clip_info['key']} does not have any audio tag metadata.")

    _database_connection.close()
    return None


def scan_clips(clips_path: Path) -> dict[str, Any]:
    """Scan audio clip files to get file information and audio metadata."""
    _all_clip_files: list[Path] = sorted(clips_path.rglob("*"))
    _all_metadata = {}

    for clip_file in _all_clip_files:
        if clip_file.is_file():
            parent: Path = clip_file.parent.relative_to(clips_path)
            key: str = str(parent / clip_file.stem)

            if key not in _all_metadata:
                _all_metadata[key] = {
                    "key": key,
                    "parent": str(parent),
                    "stem": clip_file.stem,
                    "suffixes": [
                        clip_file.suffix,
                    ],
                    "tags": parse_audio_tags(clip_file),
                }
            else:
                _all_metadata[key]["suffixes"].append(clip_file.suffix)
                if "tags" not in _all_metadata[key]:
                    _all_metadata[key]["tags"] = parse_audio_tags(clip_file)

    return _all_metadata


app_settings_path = Path("app_settings.json")
with app_settings_path.open(mode="r", encoding="utf-8") as app_settings_file:
    _app_settings: dict[str, str] = json.load(app_settings_file)

clips_directory: str | None = _app_settings.get("clips_directory")
if not clips_directory:
    sys.exit()

database_settings_path = Path("database_settings.json")
with database_settings_path.open(mode="r", encoding="utf-8") as database_settings_file:
    _database_settings = json.load(database_settings_file)

if not _database_settings:
    sys.exit()

_clips_info: dict[str, Any] = scan_clips(clips_path=Path(clips_directory))

if _clips_info:
    create_database_entries(clips_info=_clips_info, database_settings=_database_settings)
