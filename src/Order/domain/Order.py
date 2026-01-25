


from src.Infra.AggregateRoot import AggregateRoot
from src.Order.domain.OrderStatus import OrderStatus
from src.Order.domain.OrderItem import OrderItem
from src.Order.domain.events import *


class Order():
  def __init__(self, id, customer_id, items):
    self.aggregate_root = AggregateRoot()
    self.id = id
    self.customer_id = customer_id
    self.products = items
    self.status = OrderStatus.CREATE

  @classmethod
  def create(cls, id, customer_id, items):  # 최초 주문 생성
    if not items:
      raise Exception("items is empty")

    order = cls(id, customer_id, items)

    order.aggregate_root.register(OrderCreated(
        order.id,
        order.customer_id,
        order.products
    ))
    return order



  def add_item(self, item): # 최초 주문 생성 이후 아이템 추가
    if self.status == OrderStatus.COMPLETED:
      raise Exception("order status is already COMPLETED")
    if self.status == OrderStatus.CANCELLED:
      raise Exception("order status is already CANCELLED")
    if self.status == OrderStatus.SHIPPED:
      raise Exception("order status is already SHIPPED")
    if self.status == OrderStatus.PAID:
      raise Exception("order status is already PAID")
    order_item = OrderItem(item.product_id, item.price, item.quantity)
    self.products.append(order_item)

  def request_payment(self):  # 결제 요청
    if self.status == OrderStatus.COMPLETED:
      raise Exception("order status is already COMPLETED")
    if self.status == OrderStatus.CANCELLED:
      raise Exception("order status is already CANCELLED")
    if self.status == OrderStatus.SHIPPED:
      raise Exception("order status is already SHIPPED")
    if self.status == OrderStatus.PAID:
      raise Exception("order status is already PAID")
    self.status = OrderStatus.PENDINGPAYMENT
    # def __init__(self, order_id, customer_id):
    self.aggregate_root.register(OrderPaymentRequested(
        self.id,
        self.customer_id))
  def mark_as_paid(self):     # 결제 완료 처리
    if self.status == OrderStatus.COMPLETED:
      raise Exception("order status is already COMPLETED")
    if self.status == OrderStatus.CANCELLED:
      raise Exception("order status is already CANCELLED")
    if self.status == OrderStatus.SHIPPED:
      raise Exception("order status is already SHIPPED")

    self.status = OrderStatus.PAID
    total = sum(item.total() for item in self.products)
    # def __init__(self, order_id, cutomer_id):
    self.aggregate_root.register(OrderPaid(
        self.id,
        self.customer_id))
  def cancel(self):           # 주문 취소
    if self.status == OrderStatus.COMPLETED:
      raise Exception("order status is already COMPLETED")
    if self.status == OrderStatus.CANCELLED:
      raise Exception("order status is already CANCELLED")

    self.status == OrderStatus.CANCELLED
    self.aggregate_root.register(OrderCancelled(
        self.id,
        self.customer_id))
  def ship(self):             # 배송 시작
    if self.status == OrderStatus.COMPLETED:
      raise Exception("order status is already COMPLETED")
    if self.status == OrderStatus.CANCELLED:
      raise Exception("order status is already CANCELLED")
    if self.status == OrderStatus.SHIPPED:
      raise Exception("order status is already SHIPPED")
    if self.status == OrderStatus.PENDINGPAYMENT:
      raise Exception("order status is already PENDINGPAYMENT")

    self.status = OrderStatus.SHIPPED
    self.aggregate_root.register(OrderShipped(self.id))

  def complete(self):         # 주문 완료
    if self.status == OrderStatus.COMPLETED:
      raise Exception("order status is already COMPLETED")
    if self.status == OrderStatus.CANCELLED:
      raise Exception("order status is already CANCELLED")
    if self.status == OrderStatus.CREATE:
      raise Exception("order status is already CREATE")

    self.status = OrderStatus.COMPLETED
    self.aggregate_root.register(OrderCompleted(self.id))