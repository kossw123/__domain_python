from src.Order.domain.command import CreateOrder, RequestPayment, MarkOrderAsPaid, CancelOrder, ShipOrder, CompleteOrder


class OrderService():
  def __init__(self, command_bus, dispatcher, current_uow):
    self.command_bus = command_bus
    self.dispatcher = dispatcher
    self.current_uow = current_uow

  def create_order(self, order_id, customer_id, items):
    command = CreateOrder(order_id, customer_id, items)
    self._publish_command(command)
    self._publish_events()

  def request_payment(self, order_id):
    command = RequestPayment(order_id)
    self._publish_command(command)
    self._publish_events()

  def mark_as_paid(self, order_id):
    command = MarkOrderAsPaid(order_id)
    self._publish_command(command)
    self._publish_events()
    
  def cancel_order(self, order_id):
    command = CancelOrder(order_id)
    self._publish_command(command)
    self._publish_events()

  def ship_order(self, order_id):
    command = ShipOrder(order_id)
    self._publish_command(command)
    self._publish_events()

  def complete_order(self, order_id):
    command = CompleteOrder(order_id)
    self._publish_command(command)
    self._publish_events()

  def _publish_command(self, command):
    with self.current_uow:
      self.command_bus.dispatch(command)
    
  def _publish_events(self):
    while True:
      events = self.current_uow.collect_events()
      if not events:
        break
      self.dispatcher.dispatch(events)

