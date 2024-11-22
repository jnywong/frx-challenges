from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..models import Submission, Version



def leaderboard(request: HttpRequest) -> HttpResponse:
    if settings.CHALLENGE_STATE != "RUNNING":
        return HttpResponse(
            "Challenge hasn't started, so leaderboard is not available", status=400
        )

    sorted_display_config = sorted(
        settings.EVALUATION_DISPLAY_CONFIG, key=lambda dc: dc["ordering_priority"]
    )
    results = []
    all_submissions = Submission.objects.all()
    for sub in all_submissions:
        bv = sub.best_version
        if not bv:
            # Only display submissions with at least one 'best version'
            continue
        results.append({"submission": sub, "best_version": bv})

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
    return render(request, "results.html", {"results": results})
