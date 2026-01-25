from src.Product.domain.Product import Product


class ProductService():
  def __init__(self, repository, dispatcher, uow):
    self.repository = repository
    self.dispatcher = dispatcher
    self.uow = uow
  def create_product(self, id, name, price, stock):
    # product = Product(id, name, price, stock)
    # product.create_product()
    # self.repository.save(product)
    # self.__register_uow_to_dispatch(product)
    product = Product.create(id, name, price, stock)
    self.repository.save(product)
    self.__register_uow_to_dispatch(product)

  def activate_product(self, id):
    product = self.repository.find(id)
    product.activate()
    self.repository.save(product)
    self.__register_uow_to_dispatch(product)

  def decrease_stock(self, id, quantity):
    product = self.repository.find(id)
    product.decrease_stock(quantity)
    self.repository.save(product)
    self.__register_uow_to_dispatch(product)

  def increase_stock(self, id, quantity):
    product = self.repository.find(id)
    product.increase_stock(quantity)
    self.repository.save(product)
    self.__register_uow_to_dispatch(product)

  def discontinued(self, id):
    product = self.repository.find(id)
    product.discontinued()
    self.repository.save(product)
    self.__register_uow_to_dispatch(product)

  def __register_uow_to_dispatch(self, obj):
    self.uow.register(obj)
    while True:
      events = self.uow.collect_events()
      if not events:
        break
      self.dispatcher.dispatch(events)