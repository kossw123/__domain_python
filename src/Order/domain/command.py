import datetime
from src.Order.domain.Order import Order
from src.Order.domain.OrderItem import OrderItem
from src.interface.ICommand import ICommand
from src.interface.ICommandHandler import ICommandHandler



class CreateOrder(ICommand):
    def __init__(self, order_id, customer_id, items):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
class CreateOrderCommandHandler(ICommandHandler):
    def __init__(self, order_repo, product_repo, uow):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.uow = uow

    def handle(self, command: CreateOrder):
        order_items = []

        for product_id, quantity in command.items:
            product = self.product_repo.find(product_id)

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

        print("현재 주문 내역 :")
        for i in order_items:
            print(f"상품 : {i.product_id} / 가격 : {i.price} / 수량 : {i.quantity}")



class RequestPayment(ICommand):
    def __init__(self, order_id):
        self.order_id = order_id
class RequestPaymentCommandHandler(ICommandHandler):
    def __init__(self, order_repository):
        self.order_repository = order_repository
    def handle(self, command):
        order = self.order_repository.find(command.order_id)
        order.request_payment()
        self.order_repository.save(order)


class MarkOrderAsPaid(ICommand):
    def __init__(self, order_id):
        self.order_id = order_id
class MarkOrderAsPaidCommandHandler(ICommandHandler):
    def __init__(self, order_repo, uow):
        self.order_repo = order_repo
        self.uow = uow

    def handle(self, command: MarkOrderAsPaid):
        order = self.order_repo.find(command.order_id)
        order.mark_as_paid()
        self.order_repo.save(order)
        self.uow.register(order)

class CancelOrder(ICommand):
    def __init__(self, order_id):
        self.order_id = order_id
class CancelOrderCommandHandler(ICommandHandler):
    def __init__(self, order_repo, uow):
        self.order_repository
        self.uow = uow
    def handle(self, command: ICommand):
        order = self.order_repository.find(command.order_id)
        order.cancel()
        self.order_repository.save(order)
        self.uow.register(order)


class ShipOrder(ICommand):
    def __init__(self, order_id):
        self.order_id = order_id
class ShipOrderCommandHandler(ICommandHandler):
    def __init__(self, order_repo, uow):
        self.order_repo = order_repo
        self.uow = uow
    def handle(self, command: ICommand):
        order = self.order_repo.find(command.order_id)
        order.ship()
        self.order_repo.save(order)
        self.uow.register(order)


class CompleteOrder(ICommand):
    def __init__(self, order_id):
        self.order_id = order_id
class CompleteOrderCommandHandler(ICommandHandler):
    def __init__(self, order_repo, uow):
        self.order_repo = order_repo
        self.uow = uow
    def handle(self, command: ICommand):
        print(f"Complete Order CommandHandler..!")
        order = self.order_repo.find(command.order_id)
        order.complete()
        self.order_repo.save(order)
        self.uow.register(order)
        

