"""Centaur Zendo engine package.

Submodules:
    engine.config      GameConfig (all caps/timings)
    engine.sandbox     restricted exec model + subprocess sandbox workers
    engine.challenges  ChallengeSpec, ChallengeStore, validation, CompiledPool
    engine.game        game state machine
    engine.server      aiohttp server

Nothing is imported eagerly here on purpose: the engine must stay importable
(and testable) even while some submodules are still being written.
"""

__version__ = "1.0"
__all__ = ["__version__"]
