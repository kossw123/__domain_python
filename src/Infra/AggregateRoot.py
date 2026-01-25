
class AggregateRoot():
  def __init__(self):
    self.events = []
  def register(self, event):
    self.events.append(event)
  def pull_events(self):
    events = self.events
    self.events = []
    return events