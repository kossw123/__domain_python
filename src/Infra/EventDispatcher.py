from abc import ABC, abstractmethod

class IEventDispatcher(ABC):
  @abstractmethod
  def dispatch(self, events):
    pass
  @abstractmethod
  def register(self, event_type, handler):
    pass


class EventDispatcher():
  def __init__(self):
    self.handlers = {}
  def register(self, event_type, handler):
      handlers = self.handlers.setdefault(event_type, [])
      if handler not in handlers:
          handlers.append(handler)
  def dispatch(self, events):
    for event in events:
      for handler in self.handlers.get(type(event)):
        handler.handle(event)