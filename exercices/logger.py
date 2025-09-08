from __future__ import annotations

"""Simple logging utilities for exercises.

Each entry records the UTC timestamp, the exercise name and the final
score as a percentage.  Data is stored in JSON Lines format so it is easy
to append and parse.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List

LOG_FILE = Path(__file__).with_name("exercise_log.jsonl")


def log_result(exercise: str, score: float | None) -> None:
    """Append a result to the log file.

    Parameters
    ----------
    exercise:
        Name of the exercise.
    score:
        Final score as a percentage.  ``None`` may be used when the
        concept of score does not apply.
    """

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "exercise": exercise,
        "score": score,
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def get_scores(exercise: str, limit: int | None = None) -> List[float]:
    """Return past scores for ``exercise``.

    Parameters
    ----------
    exercise:
        Name of the exercise to filter in the log.
    limit:
        If provided, only the last ``limit`` scores are returned.
    """

    if not LOG_FILE.exists():
        return []

    scores: List[float] = []
    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if data.get("exercise") == exercise and isinstance(data.get("score"), (int, float)):
                scores.append(float(data["score"]))

    if limit is not None:
        scores = scores[-limit:]
    return scores
