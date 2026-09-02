"""Centaur Zendo challenge-submission web app (see SPEC.md §8).

`webapp.app.make_subapp(store, config, sandbox)` returns an aiohttp
sub-application that `engine/server.py` mounts at `/submit`; `webapp.app.main()`
runs the same app standalone.
"""

__all__ = ["app"]
