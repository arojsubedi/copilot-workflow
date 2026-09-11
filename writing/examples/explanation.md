# Explanation examples

ILLUSTRATIVE: fictional code, evidence, and results; these calibrate response shape, not the user's approved voice or facts about another repository.

## Positive: cause established

Question: Why is `completedAt` null after the export is created?

`completedAt` stays null until the worker finishes the export. Creating it only queues the job.

- `src/exports/service.py`: `ExportService.create` stores the queued state without a completion timestamp.
- `src/exports/worker.py`: `finish_export` writes the timestamp after the output is saved.

The creation response is a snapshot; refresh the export after completion to read the timestamp. `tests/exports/test_worker.py` covers the queued-to-completed transition.

## Positive: cause still uncertain

The export is still queued in the API response. That establishes why this response has no completion timestamp, but does not establish why the worker has not finished.

`ExportService.get` returns persisted state; the inspected code cannot show whether this job ran. The job's worker log would distinguish a delayed start from a failed attempt.

## Negative: conclusion buried

"I inspected the service, then the repository, then the worker. There are several stages and a few related fields to consider. After tracing them, I found that creation only queues the job."

Lead with the cause and retain the evidence needed to judge it. A deeper walkthrough can follow when requested.
