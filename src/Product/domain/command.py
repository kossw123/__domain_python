from src.interface.ICommand import ICommand
from src.interface.ICommandHandler import ICommandHandler
from src.Product.domain.Product import Product

class ProductCreate(ICommand):
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
class ProductCreateHandler(ICommandHandler):
    def __init__(self, product_repo, uow):
        self.product_repo = product_repo
        self.uow = uow
    def handle(self, command: ICommand):
        print(f"[COMMAND] ProductCreate | product_id={command.id} name={command.name} price={command.price}")
        product = Product.create(command.id, command.name, command.price)
        self.product_repo.save(product)
        self.uow.register(product)


class ProductActivate(ICommand):
    def __init__(self, id):
        self.id = id
class ProductActivateHandler(ICommandHandler):
    def __init__(self, product_repo, uow):
        self.product_repo = product_repo
        self.uow = uow
    def handle(self, command:ICommand):
        print(f"[COMMAND] ProductActivate | product_id={command.id} name={command.name} price={command.price}")
        product = self.product_repo.find(command.id)
        product.activate()
        self.product_repo.save(product)
        self.uow.register(product)




class OutOfStock(ICommand):
    def __init__(self, id, name):
        self.id = id
        self.name = name
class OutOfStockEventHandler(ICommandHandler):
    def handle(self, command:ICommand):
        print(f"[COMMAND] OutOfStock | product_id={command.id} name={command.name}")

class ProductDiscontinued(ICommand):
    def __init__(self, id, name):
        self.id = id
        self.name = name
class ProductDiscontinuedEventHandler(ICommandHandler):
    def __init__(self, product_repo, uow):
            self.product_repo = product_repo
            self.uow = uow
    def handle(self, command:ICommand):
        print(f"[COMMAND] ProductDiscontinued | product_id={command.id} name={command.name}")
        product = self.product_repo.find(command.id)
        product.discontinued()
        self.product_repo.save(product)
        self.uow.register(product)