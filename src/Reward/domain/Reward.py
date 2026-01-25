from src.Infra.AggregateRoot import AggregateRoot
from src.Reward.domain.RewardStatus import RewardStatus
from src.Reward.domain.events import RewardExpired, RewardGranted, RewardPrepared, RewardUsed


class Reward():
  def __init__(self, order_id, customer_id):
    self.aggregate_root = AggregateRoot()
    self.id = id
    self.cusomter_id = customer_id
    self.status = RewardStatus.PENDING

  @classmethod  # 보상 생성
  def create(cls, order_id, customer_id):
    if not order_id:
      raise Exception("order_id is empty")
    if not customer_id:
      raise Exception("customer_id is empty")
    reward = cls(order_id, customer_id)
    reward.aggregate_root.register(RewardPrepared(
          reward.id,
          reward.customer_id,
      ))
    return reward

  def grant(self):              # 보상 지급
    if self.status == RewardStatus.GRANTED:
      raise Exception("RewardStatus is already GRANTED")
    if self.status == RewardStatus.USED:
      raise Exception("RewardStatus is already USED")
    if self.status == RewardStatus.EXPIRED:
      raise Exception("RewardStatus is already EXPIRED")

    self.status = RewardStatus.GRANTED
    self.aggregate_root.register(RewardGranted(
        self.id,
        self.customer,
        self.pointAmount
    ))
  def use(self):                # 보상 사용
    if self.status == RewardStatus.USED:
      raise Exception("RewardStatus is already USED")
    if self.status == RewardStatus.PENDING:
      raise Exception("RewardStatus is already PENDING")
    if self.status == RewardStatus.EXPIRED:
      raise Exception("RewardStatus is already EXPIRED")

    self.status = RewardStatus.GRANTED
    self.aggregate_root.register(RewardUsed(
        self.id,
        self.customer,
        self.pointAmount
    ))
  def expire(self):             # 만료 처리
    if self.status == RewardStatus.EXPIRED:
      raise Exception("RewardStatus is already EXPIRED")
    if self.status == RewardStatus.PENDING:
      raise Exception("RewardStatus is already PENDING")
    if self.status == RewardStatus.USED:
      raise Exception("RewardStatus is already USED")

    self.status = RewardStatus.EXPIRED
    self.aggregate_root.register(RewardExpired(
        self.id,
        self.customer,
        self.pointAmount
    ))