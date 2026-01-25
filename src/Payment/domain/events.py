
from src.interface.IEvent import IEvent
from src.interface.IEventHandler import IEventHandler


class PaymentInitiated(IEvent):
  def __init__(self, id, customer_id, amount):
    self.id = id
    self.customer_id = customer_id
    self.amount = amount
class PaymentInitiatedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"PaymentInitiated: {event.id}, Customer_id: {event.customer_id}")
class PaymentAuthorized(IEvent):
  def __init__(self, id, customer_id, amount):
    self.id = id
    self.customer_id = customer_id
    self.amount = amount
class PaymentAuthorizedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"PaymentAuthorized: {event.id}, Customer_id: {event.customer_id}")
class PaymentCaptured(IEvent):
  def __init__(self, order_id, customer_id, payment_id):
    self.order_id = order_id
    self.customer_id = customer_id
    self.payment_id = payment_id
class PaymentCapturedEventHandler(IEventHandler):
  def __init__(self, reward_repository):
    self.reward_repository = reward_repository
  def handle(self, event):
    print(f"PaymentCaptured: {event.order_id}, Customer_id: {event.customer_id}")
    # reward = Reward.create()
    # self.reward_repository.save(reward)

class PaymentFailed(IEvent):
  def __init__(self, id, customer_id, amount):
    self.id = id
    self.customer_id = customer_id
    self.amount = amount
class PaymentFailedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"PaymentFailed: {event.id}, Customer_id: {event.customer_id}")
class PaymentRefunded(IEvent):
  def __init__(self, id, customer_id, amount):
    self.id = id
    self.customer_id = customer_id
    self.amount = amount
class PaymentRefundedEventHandler(IEventHandler):
  def handle(self, event):
    print(f"PaymentRefunded: {event.id}, Customer_id: {event.customer_id}")
