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
