import datetime

class IEvent():
  def __init__(self):
    self.name = self.__class__.__name__
    self.occured_at = datetime.datetime.now()