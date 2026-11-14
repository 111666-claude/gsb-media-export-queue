"""Plan replay clip exports within a render budget."""


class ExportQueue:
    def __init__(self):
        self.jobs = []
        self.Work = 0

    def apply(self, event):
        if event["op"] in ("submit", "cancel"):
            self.jobs.append(dict(event))
        else:
            raise ValueError("unknown event")

    def plan(self, now, budget):
        current = {}
        for event in self.jobs:
            self.Work += 1
            if event["op"] == "submit":
                current[event["id"]] = event
            else:
                current.pop(event["id"], None)
        chosen = []
        for job in sorted(current.values(), key=lambda j: (j["priority"], j["id"])):
            self.Work += 1
            if job["cost"] <= budget:
                chosen.append(job["id"])
        return chosen
