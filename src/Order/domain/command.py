import datetime
from src.Order.domain.Order import Order
from src.Order.domain.OrderItem import OrderItem

class ICommand():
    occured_at = datetime.datetime.now()
class CreateOrder(ICommand):
    def __init__(self, order_id, customer_id, items):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
class RequestPayment(ICommand):
    def __init__(self, order_id):
        self.order_id = order_id
class MarkOrderAsPaid(ICommand):
    def __init__(self, order_id):
        self.order_id = order_id
class CancelOrder(ICommand):
    def __init__(self, order_id):
        self.order_id = order_id
class ShipOrder(ICommand):
    def __init__(self, order_id):
        self.order_id = order_id
class CompleteOrder(ICommand):
    def __init__(self, order_id):
        self.order_id = order_id



class ICommandHandler():
    def handle(self, command: ICommand):
        pass

class CreateOrderCommandHandler(ICommandHandler):
    def __init__(self, order_repo, product_repo, uow):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.uow = uow

    def handle(self, command: CreateOrder):
        order_items = []

        for product_id, quantity in command.items:
            product = self.product_repo.find(product_id)
            product.decrease_stock(quantity)

            order_items.append(
                OrderItem.create(
                    product.id,
                    product.price,
                    quantity
                )
            )

        order = Order.create(
            command.order_id,
            command.customer_id,
            order_items
        ) 

        self.order_repo.save(order)
        self.uow.register(order)

class RequestPaymentCommandHandler(ICommandHandler):
    def __init__(self, order_repo, uow):
        self.order_repo = order_repo
        self.uow = uow

    def handle(self, command: RequestPayment):
        order = self.order_repo.find(command.order_id)
        order.request_payment()
        self.order_repo.save(order)
        self.uow.register(order)


class MarkOrderAsPaidCommandHandler(ICommandHandler):
    def __init__(self, order_repo, uow):
        self.order_repo = order_repo
        self.uow = uow

    def handle(self, command: MarkOrderAsPaid):
        order = self.order_repo.find(command.order_id)
        order.mark_as_paid()
        self.order_repo.save(order)
        self.uow.register(order)