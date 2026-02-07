from src.interface.ICommand import ICommand
from src.interface.ICommandHandler import ICommandHandler
from src.Payment.domain.Payment import Payment


class PaymentInitialize(ICommand):
    def __init__(self, order_id, customer_id, amount):
        self.order_id = order_id
        self.customer_id = customer_id
        self.amount = amount
class PaymentInitializeHandler(ICommandHandler):
    def __init__(self, payment_repo, uow):
        self.payment_repo = payment_repo
        self.uow = uow
    def handle(self, command: ICommand):
        payment = Payment.create(command.order_id, command.customer_id, command.amount)
        self.payment_repo.save(payment)
        self.uow.register(payment)


class PaymentAuthorize(ICommand):
    def __init__(self, order_id, customer_id, amount):
        self.order_id = order_id
        self.customer_id = customer_id
        self.amount = amount
class PaymentAuthorizeHandler(ICommandHandler):
    def __init__(self, payment_repo, uow):
        self.payment_repo = payment_repo
        self.uow = uow
    def handle(self, command: ICommand):
        payment = self.payment_repo.find(command.order_id)
        payment.authorize()
        self.payment_repo.save(payment)
        self.uow.register(payment)


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
        payment = self.payment_repo.find(command.order_id)
        payment.capture()
        self.payment_repo.save(payment)
        self.uow.register(payment)


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
        payment = self.payment_repo.find(command.order_id)
        payment.fail()
        self.payment_repo.save(payment)
        self.uow.register(payment)


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
        payment = self.payment_repo.find(command.order_id)
        payment.refund()
        self.payment_repo.save(payment)
        self.uow.register(payment)