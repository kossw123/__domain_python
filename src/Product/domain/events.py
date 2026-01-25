from src.interface.IEvent import IEvent
from src.interface.IEventHandler import IEventHandler


class ProductCreated(IEvent):
  def __init__(self, id, name, price):
    self.id = id
    self.name = name
    self.price = price
class ProductCreatedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"ProductCreated: {event.id}, {event.name}")
class ProductActivated(IEvent):
  def __init__(self, id, name):
    self.id = id
    self.name = name
class ProductActivatedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"ProductActivated: {event.id}, {event.name}")
class ProductStockDecreased(IEvent):
  def __init__(self, id, name, stock):
    self.id = id
    self.name = name
    self.stock = stock
class ProductStockDecreasedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"StockDecreased: {event.id}, {event.name} / remain stock : {event.stock}")
class ProductStockIncreased(IEvent):
  def __init__(self, id, name, stock):
    self.id = id
    self.name = name
    self.stock = stock
class ProductStockIncreasedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"StockIncreased: {event.id}, {event.name} / remain stock : {event.stock}")
class OutOfStock(IEvent):
  def __init__(self, id, name):
    self.id = id
    self.name = name
class OutOfStockEventHandler(IEventHandler):
  def handle(self, event):
    print(f"OutOfStock: {event.id}, {event.name}")
class ProductDiscontinued(IEvent):
  def __init__(self, id, name):
    self.id = id
    self.name = name
class ProductDiscontinuedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"ProductDiscontinued: {event.id}, {event.name}")