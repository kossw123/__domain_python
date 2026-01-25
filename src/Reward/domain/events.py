
from src.interface.IEvent import IEvent
from src.interface.IEventHandler import IEventHandler


class RewardPrepared(IEvent):
  def __init__(self, id, customer_id, point):
    self.id = id
    self.customer_id = customer_id
class RewardPreparedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"RewardPrepared: {event.id}, Customer_id: {event.customer_id}")

class RewardGranted(IEvent):
  def __init__(self, id, customer_id, point):
    self.id = id
    self.customer_id = customer_id
    self.point = point
class RewardGrantedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"RewardGranted: {event.id}, Customer_id: {event.customer_id}")
class RewardUsed(IEvent):
  def __init__(self, id, customer_id, point):
    self.id = id
    self.customer_id = customer_id
    self.point = point
class RewardUsedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"RewardUsed: {event.id}, Customer_id: {event.customer_id}")

class RewardExpired(IEvent):
  def __init__(self, id, customer_id, point):
    self.id = id
    self.customer_id = customer_id
    self.point = point
class RewardExpiredEventHandler(IEventHandler):
  def handle(self, event):
    print(f"RewardExpired: {event.id}, Customer_id: {event.customer_id}")