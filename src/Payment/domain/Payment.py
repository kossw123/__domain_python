
import uuid
from src.Infra.AggregateRoot import AggregateRoot
from src.Payment.domain.PaymentStatus import PaymentStatus
from src.Payment.domain.events import PaymentAuthorized, PaymentCaptured, PaymentFailed, PaymentInitiated, PaymentRefunded


class Payment():
  def __init__(self, customer_id, order_id, amount):
    self.aggregate_root = AggregateRoot()
    self.id = uuid.uuid4()
    self.customer_id = customer_id
    self.order_id = order_id
    self.amount = amount
    self.status = PaymentStatus.INITIALIZED

  @classmethod
  def create(cls, customer_id, order_id, amount):
    if not order_id:
      raise Exception("order_id is empty")
    if not amount and amount <= 0:
      raise Exception(f"amount is incorrect, {amount}")
    payment = cls(customer_id, order_id, amount)
    payment.aggregate_root.register(
        PaymentInitiated(payment.id,
                         payment.customer_id,
                         payment.amount))
    return payment

  # 지금은 생성과 동시에 결제를 시작하기 때문에, 아래 함수는 필요없어 보인다.
  # 그러나 결제 사전 생성 시나리오가 생겼을 때
  # 예를 들어, 카드 토큰 미리 생성 / 가상 계좌 발급 / 결제 대기 상태 유지 / 나중에 사용자가 결제버튼 클릭
  # 이런 시나리오가 생겼을 때는 분명 유용하다.
  # 하지만 현재 상태에서는 미래를 위한 추상화이기 때문에, YAGNI를 위반한다.
  # def initiate_payment(self):   # 결제 시작
  #   if self.status == PaymentStatus.AUTHORIZED:
  #     raise Exception("PaymentStatus is already AUTHORIZED")
  #   if self.status == PaymentStatus.CAPTURED:
  #     raise Exception("PaymentStatus is already CAPTURED")
  #   if self.status == PaymentStatus.FAILED:
  #     raise Exception("PaymentStatus is already FAILED")
  #   if self.status == PaymentStatus.REFUNCED:
  #     raise Exception("PaymentStatus is already REFUNCED")

  #   self.aggregate_root.register(PaymentInitiated(
  #       self.id,
  #       self.customer_id,
  #       self.amount
  #   ))
  def authorize(self):          # 승인
    if self.status == PaymentStatus.AUTHORIZED:
      raise Exception("PaymentStatus is already AUTHORIZED")
    if self.status == PaymentStatus.CAPTURED:
      raise Exception("PaymentStatus is already CAPTURED")
    if self.status == PaymentStatus.FAILED:
      raise Exception("PaymentStatus is already FAILED")
    if self.status == PaymentStatus.REFUNCED:
      raise Exception("PaymentStatus is already REFUNCED")
    if self.amount <= 0:
      raise Exception(f"amount is incorrect, {self.amount}")

    self.status = PaymentStatus.AUTHORIZED
    self.aggregate_root.register(PaymentAuthorized(
        self.id,
        self.customer_id,
        self.amount
    ))
  def capture(self):            # 결제 확정
    if self.status == PaymentStatus.CAPTURED:
      raise Exception("PaymentStatus is already CAPTURED")
    if self.status == PaymentStatus.FAILED:
      raise Exception("PaymentStatus is already FAILED")
    if self.status == PaymentStatus.REFUNCED:
      raise Exception("PaymentStatus is already REFUNCED")
    if self.amount <= 0:
      raise Exception(f"amount is incorrect, {self.amount}")

    self.status = PaymentStatus.CAPTURED
    self.aggregate_root.register(PaymentCaptured(
        self.id,
        self.customer_id,
        self.amount
    ))
  def fail(self):               # 실패 처리
    if self.status == PaymentStatus.FAILED:
      raise Exception("PaymentStatus is already FAILED")
    if self.status == PaymentStatus.REFUNCED:
      raise Exception("PaymentStatus is already REFUNCED")
    if self.status == PaymentStatus.CAPTURED:
      raise Exception("PaymentStatus is already CAPTURED")

    self.status = PaymentStatus.FAILED
    self.aggregate_root.register(PaymentFailed(
        self.id,
        self.customer_id,
        self.amount
    ))


  def refund(self):             # 환불
    if self.status == PaymentStatus.REFUNCED:
      raise Exception("PaymentStatus is already REFUNCED")
    if self.status == PaymentStatus.CAPTURED:
      raise Exception("PaymentStatus is already CAPTURED")
    if self.status == PaymentStatus.AUTHORIZED:
      raise Exception("PaymentStatus is already AUTHORIZED")

    self.status = PaymentStatus.REFUNCED
    self.aggregate_root.register(PaymentRefunded(
        self.id,
        self.customer_id,
        self.amount
    ))