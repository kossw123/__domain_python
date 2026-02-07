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