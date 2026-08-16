"""Rule-based adaptive difficulty selection for quizzes.

Deliberately simple (not IRT/ML-based): a 3-rung ladder (easy/medium/hard).
A correct answer steps up one rung, an incorrect answer steps down one rung.
This keeps the behavior easy to explain and debug, which matters more for
a hackathon MVP than statistical rigor.
"""

import random

from app.models.assessment import Difficulty

DIFFICULTY_RUNGS = [Difficulty.easy, Difficulty.medium, Difficulty.hard]


def next_difficulty(current: Difficulty, was_correct: bool) -> Difficulty:
    index = DIFFICULTY_RUNGS.index(current)
    if was_correct:
        index = min(index + 1, len(DIFFICULTY_RUNGS) - 1)
    else:
        index = max(index - 1, 0)
    return DIFFICULTY_RUNGS[index]


def pick_next_question(questions: list, asked_ids: set[str], target_difficulty: Difficulty):
    """Pick an unused question, preferring target_difficulty, falling back to the
    closest available difficulty. Returns None if the pool is exhausted."""
    unused = [q for q in questions if q.id not in asked_ids]
    if not unused:
        return None

    target_index = DIFFICULTY_RUNGS.index(target_difficulty)
    unused.sort(key=lambda q: abs(DIFFICULTY_RUNGS.index(q.difficulty) - target_index))
    closest_rank = abs(DIFFICULTY_RUNGS.index(unused[0].difficulty) - target_index)
    candidates = [q for q in unused if abs(DIFFICULTY_RUNGS.index(q.difficulty) - target_index) == closest_rank]

    return random.choice(candidates)
