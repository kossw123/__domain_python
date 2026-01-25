from src.Order.domain.events import OrderCancelled, OrderPaid, OrderPaymentRequested
from src.Payment.domain.Payment import Payment
from src.interface.ISaga import ISaga


class OrderPaymentSaga(ISaga):
  def __init__(self, order_repository, payment_repository, dispatcher, uow):
    self.order_repository = order_repository
    self.payment_repository = payment_repository
    self.dispatcher = dispatcher
    self.uow = uow

  def handle(self, event):
    if isinstance(event, OrderPaymentRequested):
      self._on_order_payment_requested(event)
    if isinstance(event, OrderPaid):
      self._on_order_paid(event)
    if isinstance(event, OrderCancelled):
      self._on_order_cancelled(event)

  def _on_order_payment_requested(self, event):
    print(f"OrderPaymentRequested: {event.order_id}, Customer_id: {event.customer_id}")
    order = self.order_repository.find(event.order_id)
    total = sum(item.total() for item in order.products)

    payment = Payment.create(event.customer_id,
                             event.order_id,
                             total)
    self.payment_repository.save(payment)
    self._process(payment)

  def _on_order_paid(self, event):
    print(f"OrderPaid: {event.order_id}, Customer_id: {event.customer_id}")
    payment = self.payment_repository.find_by_order_id(event.order_id)
    print(f"Payment Amount: {payment.amount}")
    payment.capture()
    self.payment_repository.save(payment)
    self._process(payment)
    print("Payment Captured!!")

  def _on_payment_failed(self, event):
    order = self.order_repository.find(event.order_id)
    order.cancel()
    self.order_repository.save(order)
    self._process(order)

    payment = self.payment_repository.find_by_order_id(event.order_id)
    payment.fail()
    self.payment_repository.save(payment)
    self._process(payment)
