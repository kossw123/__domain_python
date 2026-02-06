from src.Infra.EventDispatcher import EventDispatcher
from src.Infra.Repository import Repository
from src.Infra.UnitOfWork import UnitOfWork
from src.Infra.CommandBus import CommandBus
from src.Infra.Session import Session
from src.Order.application.OrderService import OrderService
from src.Payment.application.PaymentService import PaymentService
from src.Product.domain.events import *
from src.Order.domain.events import *
from src.Payment.domain.events import *
from src.Product.application.ProductService import ProductService
from src.application.saga.OrderPaymentSaga import OrderPaymentSaga
from src.Product.domain.command import (ProductCreate, ProductCreateHandler)
from src.Order.domain.command import (CompleteOrder, CompleteOrderCommandHandler, 
                                      CreateOrder, CreateOrderCommandHandler, 
                                      MarkOrderAsPaid, MarkOrderAsPaidCommandHandler, 
                                      RequestPayment, RequestPaymentCommandHandler, 
                                      ShipOrder, ShipOrderCommandHandler)




dispatcher = EventDispatcher()
command_bus = CommandBus()
session = Session()
uow = UnitOfWork(session)

product_repository = Repository()
order_repository = Repository()
payment_repository = Repository()
reward_repository = Repository()


product_service = ProductService(
    command_bus,
    dispatcher,
    uow)
order_service = OrderService(
    command_bus,
    dispatcher,
    uow)


payment_service = PaymentService(
    order_repository,
    payment_repository,
    dispatcher,
    uow
)


command_bus.register(
    CreateOrder, 
    CreateOrderCommandHandler(order_repository,
                            product_repository,
                            uow)
    )
command_bus.register(
    RequestPayment, 
    RequestPaymentCommandHandler(order_repository)
    )
command_bus.register(
    MarkOrderAsPaid,
    MarkOrderAsPaidCommandHandler(order_repository, uow)
)
command_bus.register(
    ShipOrder,
    ShipOrderCommandHandler(order_repository, uow)
)
command_bus.register(
    CompleteOrder,
    CompleteOrderCommandHandler(order_repository, uow)
)
command_bus.register(
    ProductCreate,
    ProductCreateHandler(product_repository, uow)
)





order_payment_saga = OrderPaymentSaga(
    order_repository,
    payment_repository,
    dispatcher,
    uow
)


dispatcher.register(ProductCreated, ProductCreatedEventHandler())
dispatcher.register(ProductActivated, ProductActivatedEventHandler())
dispatcher.register(ProductStockIncreased, ProductStockIncreasedEventHandler())
dispatcher.register(ProductStockDecreased, ProductStockDecreasedEventHandler())
dispatcher.register(OutOfStock, OutOfStockEventHandler())
dispatcher.register(ProductDiscontinued, ProductDiscontinuedEventHandler())

dispatcher.register(OrderCreated, OrderCreatedEventHandler())
dispatcher.register(OrderPaymentRequested, order_payment_saga)
dispatcher.register(OrderPaid, order_payment_saga)
dispatcher.register(OrderCancelled, OrderCancelledEventHandler())
dispatcher.register(OrderShipped, OrderShippedEventHandler())
dispatcher.register(OrderCompleted, OrderCompletedEventHandler())

dispatcher.register(PaymentInitiated, PaymentInitiatedEventHandler())
dispatcher.register(PaymentAuthorized, PaymentAuthorizedEventHandler())
dispatcher.register(PaymentCaptured, PaymentCapturedEventHandler(reward_repository))
dispatcher.register(PaymentFailed, PaymentFailedEventHandler())
dispatcher.register(PaymentRefunded, PaymentRefundedEventHandler())

# dispatcher.register(RewardPrepared, RewardPreparedEventHandler())
# dispatcher.register(RewardGranted, RewardGrantedEventHandler())
# dispatcher.register(RewardUsed, RewardUsedEventHandler())
# dispatcher.register(RewardExpired, RewardExpiredEventHandler())



product_service.create_product(1, 'Americano', 3000)
product_service.create_product(2, 'Caffelatte', 4000)
product_service.create_product(3, 'Caramel Macchiato', 5000)
product_service.create_product(4, 'Mint Tea', 4000)

# product_service.activate_product(1)
# product_service.activate_product(2)
# product_service.activate_product(3)
# product_service.activate_product(4)



items = [
    [1,4],
    [2,3],
    [3,1]
]

order_service.create_order(order_id := 1, customer_id := 1, items)
order_service.request_payment(order_id)
order_service.mark_as_paid(order_id)
order_service.ship_order(order_id)
order_service.complete_order(order_id)
