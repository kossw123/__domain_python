from src.Order.domain.events import OrderCancelled, OrderPaid, OrderPaymentRequested
from src.Order.domain.command import OrderCreate
from src.Payment.domain.Payment import Payment
from src.Payment.domain.events import PaymentInitiated, PaymentCaptured, PaymentFailed
from src.interface.ISaga import ISaga

class Legacy(ISaga):
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


# Saga는 이벤트를 보고 커맨드를 결정한다.
# 즉, 이벤트를 invoke한 다음 Command를 생성한다.
# 도메인간 분기가 생기거나, 실패/보상의 흐름이 있는 지점에 Saga가 생성되어야 한다.
#region Command Refactoring
# Saga는 스스로 실행되지 않는다.
# EventDispatcher에 등록된 특수한 EventHandler로 실행된다.
# Order <-> Payment간 어떤 실패 흐름이 존재할까?
class CurrentOrderPaymentSaga(ISaga):
    def __init__(self, command_bus):
        self.command_bus = command_bus

    def handle(self, event):
        if isinstance(event, OrderPaymentRequested):
            self._on_order_payment_requested(event)
        if isinstance(event, OrderPaid):
            self._on_order_paid(event)
        if isinstance(event, OrderCancelled):
            self._on_order_cancelled(event)

    def _on_order_payment_requested(self, event):
        self.command_bus.dispatch(
            PaymentInitiated(
            customer_id=event.customer_id,
            order_id=event.order_id
            )
        )
    def _on_order_paid(self, event):
        self.command_bus.dispatch(
            PaymentCaptured(order_id=event.order_id)
        )

    def _on_payment_failed(self, event):
        self.command_bus.dispatch(
            PaymentFailed(order_id=event.order_id)
        )

#endregion