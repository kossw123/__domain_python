from abc import ABC, abstractmethod

class ISaga(ABC):
  @abstractmethod
  def handle(self, event):
    pass
  def _process(self, aggregate):
    self.uow.register(aggregate)

    while True:
      events = self.uow.collect_events()
      if not events:
        break;

    self.dispatcher.dispatch(events)