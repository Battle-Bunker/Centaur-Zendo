"""GameConfig — every cap, timing and knob of the Centaur Zendo engine (SPEC §2/§3/§5).

All values live here so the game can be re-tuned from one JSON file:

    cfg = GameConfig.load("game.example.json")   # path, dict or None
    cfg.to_dict()                                # full round-trippable dict
    cfg.public_dict()                            # subset sent in welcome.config
"""
from __future__ import annotations

import dataclasses
import json
import logging
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, Mapping

log = logging.getLogger("centaur.config")

__all__ = ["GameConfig"]


@dataclass
class GameConfig:
    """Configuration for one game. Every field is JSON-serialisable."""

    # ---- round / phase timing (SPEC §5) -------------------------------------
    round_seconds: float = 1.0            # training round length
    final_seconds: float = 3.0            # final test round length
    cooldown_seconds: float = 300.0       # min gap start->start between a team's rounds
    max_training_rounds: int = 12         # hard cap per team
    training_seconds: float | None = None  # None => max_training_rounds*cooldown+60
    final_window_seconds: float = 600.0   # how long the final stays open
    demo_per_window: int = 1              # demos allowed per cooldown window

    # ---- game behaviour -----------------------------------------------------
    open_registration: bool = True        # unknown teams auto-created on join
    challenge_dir: str = "challenges"
    event_log: str = "events.jsonl"
    sandbox_workers: int = 4
    final_shared_sequence: bool = True    # every team faces the same (name, seed) run
    final_seed: int | None = 20250601     # seed of that shared sequence (None => random at final start)

    # ---- code size caps (SPEC §2) -------------------------------------------
    max_score_code_chars: int = 256
    max_clue_chars: int = 1024
    max_generate_code_chars: int = 50_000
    max_solve_code_chars: int = 5_000
    max_solution_chars: int = 4096

    # ---- per-call wall-clock caps, milliseconds (SPEC §2) --------------------
    max_generate_ms: int = 100
    max_score_ms: int = 50
    max_solve_ms: int = 2000

    # ---- validation (SPEC §4) ----------------------------------------------
    validation_seeds: int = 20
    validation_seed: int = 12345

    # ---- server -------------------------------------------------------------
    host: str = "0.0.0.0"
    port: int = 8080
    admin_token: str = ""

    # ------------------------------------------------------------------ setup
    def __post_init__(self) -> None:
        # Numeric fields arriving from JSON may be ints where floats are wanted
        # (and vice versa); normalise so later arithmetic/serialisation is boring.
        for f in fields(self):
            v = getattr(self, f.name)
            if v is None:
                continue
            if f.type in ("float", "float | None"):
                setattr(self, f.name, float(v))
            elif f.type in ("int", "int | None"):
                setattr(self, f.name, int(v))
            elif f.type == "bool":
                setattr(self, f.name, bool(v))
            elif f.type == "str":
                setattr(self, f.name, str(v))
        # SPEC §5: training_seconds = None => max_training_rounds*cooldown + 60.
        # Resolved eagerly so every consumer sees a concrete number.
        if self.training_seconds is None:
            self.training_seconds = float(self.max_training_rounds) * float(self.cooldown_seconds) + 60.0
        self.validate()

    def validate(self) -> None:
        """Raise ValueError on nonsensical values (cheap sanity, not a schema)."""
        problems = []
        if self.round_seconds <= 0 or self.final_seconds <= 0:
            problems.append("round_seconds and final_seconds must be > 0")
        if self.cooldown_seconds < 0:
            problems.append("cooldown_seconds must be >= 0")
        if self.max_training_rounds < 0:
            problems.append("max_training_rounds must be >= 0")
        if self.sandbox_workers < 1:
            problems.append("sandbox_workers must be >= 1")
        if self.validation_seeds < 1:
            problems.append("validation_seeds must be >= 1")
        for name in ("max_score_code_chars", "max_clue_chars", "max_generate_code_chars",
                     "max_solve_code_chars", "max_solution_chars",
                     "max_generate_ms", "max_score_ms", "max_solve_ms"):
            if getattr(self, name) <= 0:
                problems.append(f"{name} must be > 0")
        if problems:
            raise ValueError("invalid GameConfig: " + "; ".join(problems))

    # ------------------------------------------------------------------ loading
    @classmethod
    def load(cls, path_or_dict: "str | Path | Mapping[str, Any] | GameConfig | None" = None) -> "GameConfig":
        """Build a config from a JSON file path, a mapping, another config, or nothing.

        Unknown keys are ignored with a warning so an old config file never stops
        the server from booting.
        """
        if path_or_dict is None:
            return cls()
        if isinstance(path_or_dict, GameConfig):
            return cls.from_dict(path_or_dict.to_dict())
        if isinstance(path_or_dict, Mapping):
            return cls.from_dict(path_or_dict)
        path = Path(path_or_dict)
        with path.open() as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError(f"{path}: config JSON must be an object")
        return cls.from_dict(data, source=str(path))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any], source: str = "<dict>") -> "GameConfig":
        known = {f.name for f in fields(cls)}
        kwargs = {k: v for k, v in data.items() if k in known}
        unknown = sorted(set(data) - known)
        if unknown:
            log.warning("%s: ignoring unknown config keys: %s", source, ", ".join(unknown))
        return cls(**kwargs)

    def replace(self, **changes: Any) -> "GameConfig":
        """A copy with some fields changed (handy in tests)."""
        return dataclasses.replace(self, **changes)

    # ------------------------------------------------------------------ output
    def to_dict(self) -> dict[str, Any]:
        """Full config as a plain dict (round-trips through GameConfig.load)."""
        return dataclasses.asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=False)

    def save(self, path: "str | Path") -> None:
        Path(path).write_text(self.to_json() + "\n")

    def public_dict(self, training_ends_at: float | None = None,
                    final_ends_at: float | None = None) -> dict[str, Any]:
        """The `config` object inside a `welcome` frame (SPEC §6).

        `training_ends_at` / `final_ends_at` are runtime values owned by the game;
        they are always present as keys (None until the game starts).
        """
        return {
            "round_seconds": self.round_seconds,
            "final_seconds": self.final_seconds,
            "cooldown_seconds": self.cooldown_seconds,
            "max_training_rounds": self.max_training_rounds,
            "max_solution_chars": self.max_solution_chars,
            "max_clue_chars": self.max_clue_chars,
            "training_ends_at": training_ends_at,
            "final_ends_at": final_ends_at,
        }

    def caps_dict(self) -> dict[str, Any]:
        """Author-facing caps (webapp GET /api/config, tools/quickcheck CAPS)."""
        return {
            "max_score_code_chars": self.max_score_code_chars,
            "max_clue_chars": self.max_clue_chars,
            "max_generate_code_chars": self.max_generate_code_chars,
            "max_solve_code_chars": self.max_solve_code_chars,
            "max_solution_chars": self.max_solution_chars,
            "max_generate_ms": self.max_generate_ms,
            "max_score_ms": self.max_score_ms,
            "max_solve_ms": self.max_solve_ms,
            "validation_seeds": self.validation_seeds,
            "validation_seed": self.validation_seed,
        }

    # ------------------------------------------------------------------ helpers
    @property
    def training_duration(self) -> float:
        """Resolved training length in seconds (never None)."""
        if self.training_seconds is None:  # pragma: no cover - resolved in __post_init__
            return float(self.max_training_rounds) * float(self.cooldown_seconds) + 60.0
        return float(self.training_seconds)

    @property
    def round_ms(self) -> int:
        return int(round(self.round_seconds * 1000))

    @property
    def final_ms(self) -> int:
        return int(round(self.final_seconds * 1000))
