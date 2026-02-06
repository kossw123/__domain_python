from src.interface.ICommand import ICommand
from src.interface.ICommandHandler import ICommandHandler

#   INITIALIZED = 0
#   AUTHORIZED = 1
#   CAPTURED = 2
#   FAILED = 3
#   REFUNCED = 4


class PaymentInitialize(ICommand):
    def __init__(self, id, customer_id, amount):
        self.id = id
        self.customer_id = customer_id
        self.amount = amount
class PaymentInitializeHandler(ICommandHandler):
    def __init__(self, payment_repo, uow):
        self.payment_repo = payment_repo
        self.uow = uow
    def handle(self, command: ICommand):
        pass


class PaymentAuthorize(ICommand):
    def __init__(self, id, customer_id, amount):
        self.id = id
        self.customer_id = customer_id
        self.amount = amount
class PaymentAuthorizeHandler(ICommandHandler):
    def __init__(self, payment_repo, uow):
        self.payment_repo = payment_repo
        self.uow = uow
    def handle(self, command: ICommand):
        pass


class PaymentCapture(ICommand):
    def __init__(self, order_id, customer_id, payment_id):
        self.order_id = order_id
        self.customer_id = customer_id
        self.payment_id = payment_id
class PaymentCaptureHandler(ICommandHandler):
    def __init__(self, payment_repo, uow):
        self.payment_repo = payment_repo
        self.uow = uow
    def handle(self, command: ICommand):
        pass


class PaymentFail(ICommand):
    def __init__(self, id, customer_id, amount):
        self.id = id
        self.customer_id = customer_id
        self.amount = amount
class PaymentFailHandler(ICommandHandler):
    def __init__(self, payment_repo, uow):
        self.payment_repo = payment_repo
        self.uow = uow
    def handle(self, command: ICommand):
        pass


class PaymentRefund(ICommand):
    def __init__(self, id, customer_id, amount):
        self.id = id
        self.customer_id = customer_id
        self.amount = amount
class PaymentRefundHandler(ICommandHandler):
    def __init__(self, payment_repo, uow):
        self.payment_repo = payment_repo
        self.uow = uow
    def handle(self, command: ICommand):
        pass