from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..models import Submission, Version


def leaderboard(request: HttpRequest) -> HttpResponse:
    if settings.CHALLENGE_STATE != "RUNNING":
        return HttpResponse(
            "Challenge hasn't started, so leaderboard is not available", status=400
        )

    if settings.SITE_LEADERBOARD_DESCRIPTION:
        description = settings.SITE_LEADERBOARD_DESCRIPTION
    else:
        description = "This is the leaderboard for this challenge."

    sorted_display_config = sorted(
        settings.EVALUATION_DISPLAY_CONFIG, key=lambda dc: dc["ordering_priority"]
    )
    results = []
    all_submissions = Submission.objects.all()
    for sub in all_submissions:
        # Get best scoring version
        bv = sub.best_version
        if not bv:
            # Only display submissions with at least one 'best version'
            continue
        # Get submission metadata
        metadata = []
        for k, v in settings.SITE_SUBMISSION_FORM_SCHEMA["properties"].items():
            if v.get("leaderboard_display"):
                metadata.append(
                    sub.metadata.get(k),
                )
        results.append(
            {
                "submission": sub,
                "best_version": bv,
                "metadata": metadata,
            }
        )

    def sort_key_func(r):
        bv: Version = r["best_version"]
        sort_key = []
        for dc in sorted_display_config:
            if dc["ordering"] == "ascending":
                sort_key.append(-bv.latest_evaluation.result[dc["result_key"]])
            elif dc["ordering"] == "descending":
                sort_key.append(bv.latest_evaluation.result[dc["result_key"]])
            else:
                raise ValueError(
                    f"Invalid ordering {dc['ordering']} found for result_key {dc['result_key']}"
                )

        return sort_key

    results = sorted(results, key=sort_key_func)

    metadata_display = []
    for k, v in settings.SITE_SUBMISSION_FORM_SCHEMA["properties"].items():
        if v.get("leaderboard_display"):
            metadata_display.append(v.get("title"))

    return render(
        request,
        "results.html",
        {
            "results": results,
            "description": description,
            "metadata_display": metadata_display,
        },
    )
