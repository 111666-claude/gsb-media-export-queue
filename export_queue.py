"""Plan replay clip exports within a render budget."""


class ExportQueue:
    def __init__(self):
        # Effective state, maintained incrementally so plan() never rescans
        # cancelled or superseded history.
        self.current = {}     # id -> effective submit event
        self.tombstones = {}  # id -> highest cancel revision seen
        self.Work = 0

    def apply(self, event):
        op = event["op"]
        if op == "submit":
            job_id = event["id"]
            revision = event["revision"]
            tombstone = self.tombstones.get(job_id)
            if tombstone is not None and revision <= tombstone:
                return  # cancelled at a >= revision: tombstone wins
            existing = self.current.get(job_id)
            if existing is None or revision > existing["revision"]:
                self.current[job_id] = dict(event)
        elif op == "cancel":
            job_id = event["id"]
            revision = event["revision"]
            existing = self.current.get(job_id)
            if existing is not None and revision >= existing["revision"]:
                del self.current[job_id]
            tombstone = self.tombstones.get(job_id)
            if tombstone is None or revision > tombstone:
                self.tombstones[job_id] = revision
        else:
            raise ValueError("unknown event")

    def plan(self, now, budget):
        ready = [job for job in self.current.values() if job["ready"] <= now]
        ready.sort(key=lambda j: (-j["priority"], j["id"]))
        chosen = []
        remaining = budget
        for job in ready:
            self.Work += 1
            if job["cost"] <= remaining:
                chosen.append(job["id"])
                remaining -= job["cost"]
        return chosen
