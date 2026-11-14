# Replay clip export queue

Render jobs arrive as `submit` events with ID, revision, ready tick, cost, and
priority; `cancel` events carry ID and revision. For each ID, only the highest
revision is effective, and cancellation is a tombstone. A plan at tick `now`
may select ready, non-cancelled jobs. It ranks higher priority first, then ID,
accepting a job only if its whole cost fits the **remaining** budget. A plan
does not itself remove jobs, so repeated calls with the same state are stable.

`Work` counts jobs inspected by plan calls. Once jobs have been cancelled or
superseded, future plans must not repeatedly rescan their history.
