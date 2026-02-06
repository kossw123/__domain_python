from src.Order.domain.command import CreateOrder, RequestPayment, MarkOrderAsPaid, CancelOrder, ShipOrder, CompleteOrder
from contextlib import contextmanager

class OrderService():
    def __init__(self, command_bus, dispatcher, uow):
        self.command_bus = command_bus
        self.dispatcher = dispatcher
        self.uow = uow

    def create_order(self, order_id, customer_id, items):
        with self.command_context():
            self.command_bus.dispatch(CreateOrder(order_id, customer_id, items))

    def request_payment(self, order_id):
        with self.command_context():
            self.command_bus.dispatch(RequestPayment(order_id))

    def mark_as_paid(self, order_id):
        with self.command_context():
            self.command_bus.dispatch(MarkOrderAsPaid(order_id))
        
    def cancel_order(self, order_id):
        with self.command_context():
            self.command_bus.dispatch(CancelOrder(order_id))

    def ship_order(self, order_id):
        with self.command_context():
            self.command_bus.dispatch(ShipOrder(order_id))

    def complete_order(self, order_id):
        with self.command_context():
            self.command_bus.dispatch(CompleteOrder(order_id))



    def _publish_events(self):
        while True:
            events = self.uow.collect_events()
            if not events:
                break
            self.dispatcher.dispatch(events)
    @contextmanager
    def command_context(self):
        with self.uow:
            yield
        self._publish_events()

