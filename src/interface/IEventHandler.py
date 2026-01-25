from abc import ABC, abstractmethod

class IEventHandler(ABC):
  @abstractmethod
  def handle(self, event):
    pass
