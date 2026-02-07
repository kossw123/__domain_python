from contextlib import contextmanager
from src.Payment.domain.command import (PaymentAuthorize,
                                        PaymentCapture,
                                        PaymentFail,
                                        PaymentRefund)


class Legacy():
  def __init__(self, order_repository, payment_repository, dispatcher, uow):
    self.order_repository = order_repository
    self.payment_repository = payment_repository
    self.dispatcher = dispatcher
    self.uow = uow

  # payment.initiate_payment()가 YAGNI 위반에 따라
  # 삭제됨에 따라 해당 행동도 필요가 없어졌다.
  # def initiate_payment(self, id, customer_id, order_id):
  #   payment = payment_repository.find(id)
  #   payment.initiate_payment()
  #   self.payment_repository.save(payment)
  #   self.__register_uow_to_dispatch(payment)


  def authorize(self, id):
    payment = self.payment_repository.find_by_order_id(id)
    payment.authorize()
    self.payment_repository.save(payment)
    self.__register_uow_to_dispatch(payment)
  def capture(self, id):
    payment = self.payment_repository.find(id)
    payment.capture()
    self.payment_repository.save(payment)
    self.__register_uow_to_dispatch(payment)
  def fail(self, id):
    payment = self.payment_repository.find(id)
    payment.fail()
    self.payment_repository.save(payment)
    self.__register_uow_to_dispatch(payment)
  def refund(self, id):
    payment = self.payment_repository.find(id)
    payment.refund()
    self.payment_repository.save(payment)
    self.__register_uow_to_dispatch(payment)
  def __register_uow_to_dispatch(self, obj):
    self.uow.register(obj)
    while True:
      events = self.uow.collect_events()
      if not events:
        break
      self.dispatcher.dispatch(events)


from contextlib import contextmanager
from src.Payment.domain.command import (PaymentAuthorize,
                                        PaymentCapture,
                                        PaymentFail,
                                        PaymentRefund)


class PaymentService():
    def __init__(self, command_bus, dispatcher, uow):
        self.command_bus = command_bus
        self.dispatcher = dispatcher
        self.uow = uow

    def authorize(self, id):
        with self.command_context():
            self.command_bus.dispatch(PaymentAuthorize(id))
    def capture(self, order_id, customer_id, payment_id):
        with self.command_context():
            self.command_bus.dispatch(PaymentCapture(order_id, customer_id, payment_id))
    def fail(self, id, customer_id, amount):
        with self.command_context():
            self.command_bus.dispatch(PaymentFail(id, customer_id, amount))
    def refund(self, id, customer_id, amount):
        with self.command_context():
            self.command_bus.dispatch(PaymentRefund(id, customer_id, amount))

    @contextmanager
    def command_context(self):
        with self.uow:
            yield
        self._publish_events()

    def _publish_events(self):
        while True:
            events = self.uow.collect_events()
            if not events:
                break
            self.dispatcher.dispatch(events)