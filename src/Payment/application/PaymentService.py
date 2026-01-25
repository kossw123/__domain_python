
class PaymentService():
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