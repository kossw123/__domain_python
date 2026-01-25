
from src.Order.domain.Order import Order
from src.Order.domain.OrderItem import OrderItem


class OrderService():
  def __init__(self, order_repository, product_repository, dispatcher, uow):
    self.order_repository = order_repository
    self.product_repository = product_repository
    self.dispatcher = dispatcher
    self.uow = uow

  # def add_item(self, order_id, product_id, quantity):
  #   product = self.product_repository.find(product_id)
  #   order = self.order_repository.find(order_id)


  #   extractItem = OrderItem(product.name, product.price, quantity)
  #   order.add_item(extractItem)
  #   self.order_repository.save(order)

  #   product.decrease_stock(quantity)
  #   self.product_repository.save(product)

  def create_order(self, order_id, customer_id, items):
    order_items = []

    # id, name, price, stock
    for product_id, quantity in items:
      product = self.product_repository.find(product_id)
      product.decrease_stock(quantity)

      order_items.append(
          OrderItem.create(
              product.id,
              product.price,
              quantity))


    order = Order.create(order_id, customer_id, order_items)
    self.order_repository.save(order)
    self.__register_uow_to_dispatch(order)


  def request_payment(self, id):
    order = self.order_repository.find(id)

    order.request_payment()

    self.order_repository.save(order)
    self.__register_uow_to_dispatch(order)

  def mark_as_paid(self, id):
    order = self.order_repository.find(id)

    order.mark_as_paid()

    self.order_repository.save(order)
    self.__register_uow_to_dispatch(order)

  def cancel(self, id):
    order = self.order_repository.find(id)

    order.cancel()

    self.order_repository.save(order)
    self.__register_uow_to_dispatch(order)

  def ship(self, id):
    order = self.order_repository.find(id)

    order.ship()

    self.order_repository.save(order)
    self.__register_uow_to_dispatch(order)

  def complete(self, id):
    order = self.order_repository.find(id)
    order.complete()

    self.order_repository.save(order)
    self.__register_uow_to_dispatch(order)

  def __register_uow_to_dispatch(self, obj):
    self.uow.register(obj)
    while True:
      events = self.uow.collect_events()
      if not events:
        break
      self.dispatcher.dispatch(events)