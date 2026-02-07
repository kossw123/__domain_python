from src.interface.IEvent import IEvent
from src.interface.IEventHandler import IEventHandler


class ProductCreated(IEvent):
  def __init__(self, id, name, price):
    self.id = id
    self.name = name
    self.price = price
class ProductCreatedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"[EVENT] ProductCreate | product_id={event.id} name={event.name} price={event.price}")
class ProductActivated(IEvent):
  def __init__(self, id, name):
    self.id = id
    self.name = name
class ProductActivatedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"[EVENT] ProductActivated | product_id={event.id} name={event.name}")

class OutOfStock(IEvent):
  def __init__(self, id, name):
    self.id = id
    self.name = name
class OutOfStockEventHandler(IEventHandler):
  def handle(self, event):
    print(f"[EVENT] OutOfStock | product_id={event.id} name={event.name}")
class ProductDiscontinued(IEvent):
  def __init__(self, id, name):
    self.id = id
    self.name = name
class ProductDiscontinuedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"[EVENT] ProductDiscontinued | product_id={event.id} name={event.name}")