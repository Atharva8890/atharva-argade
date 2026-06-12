"""Cinematic motivational documentary renderer.

A self-contained pipeline that turns a timed narration storyboard into a
premium, CapCut-Pro-style motivational documentary video:

    narration (neural TTS)  ->  timed storyboard  ->  cinematic frame compositor
    +  animated keyword captions  +  procedural orchestral score  ->  final mp4

See ``render.py`` for the command line entry point and ``README.md`` for usage.
"""

__all__ = [
    "config",
    "script",
    "narration",
    "scenes",
    "effects",
    "captions",
    "music",
    "compositor",
]
