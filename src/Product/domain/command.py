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
        print(f"Product Create Command 발생!!")
        product = Product.create(command.id, command.name, command.price)
        self.product_repo.save(product)
        self.uow.register(product)
        print("선택된 상품을 등록했습니다.")


class ProductActivate(ICommand):
    def __init__(self, id):
        self.id = id
class ProductActivateHandler(ICommandHandler):
    def __init__(self, product_repo, uow):
        self.product_repo = product_repo
        self.uow = uow
    def handle(self, command:ICommand):
        print(f"Product Activate 발생!! : [{command.id}]")
        product = self.product_repo.find(command.id)
        product.activate()
        self.product_repo.save(product)
        self.uow.register(product)
        print("선택된 상품이 활성화 되었습니다.")




class OutOfStock(ICommand):
    def __init__(self, id, name):
        self.id = id
        self.name = name
class OutOfStockEventHandler(ICommandHandler):
    def handle(self, command:ICommand):
        print(f"Out Of Stock : 발생!! : [{command.id}, {command.name}, {command.stock}]")

class ProductDiscontinued(ICommand):
    def __init__(self, id, name):
        self.id = id
        self.name = name
class ProductDiscontinuedEventHandler(ICommandHandler):
    def __init__(self, product_repo, uow):
            self.product_repo = product_repo
            self.uow = uow
    def handle(self, command:ICommand):
        print(f"Product Discontinue 발생!! : {command.id}, {command.name}")
        product = self.product_repo.find(command.id)
        product.discontinued()
        self.product_repo.save(product)
        self.uow.register(product)
        print("선택된 상품이 비활성화 되었습니다.")