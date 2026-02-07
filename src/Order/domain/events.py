
from src.Payment.domain.Payment import Payment
from src.interface.IEvent import IEvent
from src.interface.IEventHandler import IEventHandler


class OrderCreated(IEvent):
  def __init__(self, id, customer_id, products):
    self.id = id
    self.customer_id = customer_id
    self.products = products

class OrderCreatedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"[EVENT] OrderCreated | order_id={event.id} customer_id={event.customer_id}")
    print(f"   현재 주문된 내역")
    for item in event.products:
      print(f"      Product_id:{item.product_id} | Quantity:{item.quantity} | total:{item.total()}")
      
class OrderPaymentRequested(IEvent):
  def __init__(self, order_id, customer_id):
    self.order_id = order_id
    self.customer_id = customer_id
class OrderPaymentRequestedEventHandler(IEventHandler):
  def __init__(self, order_repository, payment_repository, dispathcer, uow):
    self.order_repository = order_repository
    self.payment_repository = payment_repository
    self.dispathcer = dispathcer
    self.uow = uow
  def handle(self, event):
    print(f"[EVENT] OrderPaymentRequested | order_id={event.order_id} customer_id={event.customer_id}")
    order = self.order_repository.find(event.order_id)
    total = sum(item.total() for item in order.products)

    # def create(cls, customer_id, order_id, amount):
    payment = Payment.create(event.customer_id,
                             event.order_id,
                             total)
    self.payment_repository.save(payment)
    self.__register_uow_to_dispatch(payment)

  def __register_uow_to_dispatch(self, obj):
    self.uow.register(obj)
    while True:
      events = self.uow.collect_events()
      if not events:
        break
      self.dispatcher.dispatch(events)


class OrderPaid(IEvent):
  def __init__(self, order_id, customer_id):
    self.order_id = order_id
    self.customer_id = customer_id
class OrderPaidEventHandler(IEventHandler):
  def __init__(self, payment_repository):
    self.payment_repository = payment_repository
  def handle(self, event):
    print(f"[EVENT] OrderPaid | order_id={event.order_id} customer_id={event.customer_id}")
    payment = self.payment_repository.find_by_order_id(event.order_id)

    if not payment:
      raise Exception("payment not found")
    
    print(f"    Amount: {payment.amount}")
    payment.authorize()
    self.payment_repository.save(payment)


class OrderCancelled(IEvent):
  def __init__(self, id, customer_id):
    self.id = id
    self.customer_id = customer_id
class OrderCancelledEventHandler(IEventHandler):
  def handle(self, event):
    print(f"[EVENT] OrderCancelled | order_id={event.id}")
class OrderShipped(IEvent):
  def __init__(self, id):
    self.id = id
class OrderShippedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"[EVENT] OrderShipped | order_id={event.id}")
class OrderCompleted(IEvent):
  def __init__(self, id):
    self.id = id
class OrderCompletedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"[EVENT] OrderCompleted | order_id={event.id}")
