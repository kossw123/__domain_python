from contextlib import contextmanager
from src.Product.domain.command import (
    ProductCreate,
    ProductActivate,
    ProductDiscontinued
)



class ProductService():
    def __init__(self, command_bus, dispatcher, uow):
        self.command_bus = command_bus
        self.dispatcher = dispatcher
        self.uow = uow

    def create_product(self, id, name, price):
        with self.command_context():
            self.command_bus.dispatch(ProductCreate(id, name, price))

    def activate_product(self, id):
        with self.command_context():
            self.command_bus.dispatch(ProductActivate(id))

    def discontinue_product(self, id):
        with self.command_context():
            self.command_bus.dispatch(ProductDiscontinued(id))
        
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