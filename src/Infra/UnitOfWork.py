
class UnitOfWork():
  def __init__(self):
    self.seen = set()
  def register(self, aggregate):
    self.seen.add(aggregate)
  def collect_events(self):
    events = []
    for aggregate in self.seen:
      events.extend(aggregate.aggregate_root.pull_events())
    return events
