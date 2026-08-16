"""Skill-gap -> job-readiness matching.

Deliberately a hand-set weighted average, not a trained model: the scoring
is fully explainable (a learner or admin can see exactly why a readiness
number is what it is), which matters more for this MVP than statistical
sophistication. Only worth reaching for scikit-learn if this simple version
demonstrably falls short — see DECISIONS.md.
"""

from app.models.assessment import SkillCategory

JOB_PROFILES = [
    {
        "id": "retail-customer-service",
        "title": "Retail / Customer Service Associate",
        "weights": {
            SkillCategory.communication: 0.35,
            SkillCategory.digital_literacy: 0.25,
            SkillCategory.workplace_professionalism: 0.25,
            SkillCategory.problem_solving: 0.15,
        },
    },
    {
        "id": "data-entry-back-office",
        "title": "Data Entry / Back-Office Assistant",
        "weights": {
            SkillCategory.digital_literacy: 0.40,
            SkillCategory.problem_solving: 0.25,
            SkillCategory.workplace_professionalism: 0.20,
            SkillCategory.communication: 0.15,
        },
    },
    {
        "id": "administrative-assistant",
        "title": "Administrative / Office Assistant",
        "weights": {
            SkillCategory.communication: 0.30,
            SkillCategory.digital_literacy: 0.25,
            SkillCategory.workplace_professionalism: 0.25,
            SkillCategory.financial_literacy: 0.20,
        },
    },
    {
        "id": "community-outreach-worker",
        "title": "Community Outreach Worker",
        "weights": {
            SkillCategory.communication: 0.40,
            SkillCategory.workplace_professionalism: 0.25,
            SkillCategory.problem_solving: 0.20,
            SkillCategory.digital_literacy: 0.15,
        },
    },
    {
        "id": "microenterprise-support-worker",
        "title": "Microenterprise Support Worker",
        "weights": {
            SkillCategory.financial_literacy: 0.35,
            SkillCategory.communication: 0.25,
            SkillCategory.problem_solving: 0.20,
            SkillCategory.digital_literacy: 0.20,
        },
    },
]


def compute_category_scores(
    best_scores_by_quiz_category: list[tuple[SkillCategory, float]],
) -> dict[SkillCategory, float]:
    """Average a learner's best-attempt scores per skill category.

    Input is (category, best_score_pct) pairs, one per attempted, tagged
    quiz. A category with no attempts is simply absent from the result —
    callers treat a missing category as 0 when scoring job readiness.
    """
    totals: dict[SkillCategory, list[float]] = {}
    for category, score in best_scores_by_quiz_category:
        totals.setdefault(category, []).append(score)
    return {category: sum(scores) / len(scores) for category, scores in totals.items()}


def compute_job_readiness(category_scores: dict[SkillCategory, float]) -> list[dict]:
    """Weighted-average readiness % per job profile, plus a "focus next on X"
    recommendation: the required category with the largest weighted gap
    (weight x (100 - score)), i.e. the category that would move the needle
    most if improved."""
    results = []
    for profile in JOB_PROFILES:
        weights = profile["weights"]
        readiness_pct = sum(weights[cat] * category_scores.get(cat, 0.0) for cat in weights)

        focus_category = max(
            weights, key=lambda cat: weights[cat] * (100 - category_scores.get(cat, 0.0))
        )

        results.append(
            {
                "job_id": profile["id"],
                "title": profile["title"],
                "readiness_pct": round(readiness_pct, 1),
                "focus_next": focus_category.value,
            }
        )
    return sorted(results, key=lambda r: r["readiness_pct"], reverse=True)
