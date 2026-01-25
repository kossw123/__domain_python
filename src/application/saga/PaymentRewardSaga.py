

from src.interface.ISaga import ISaga


class PaymentRewardSaga(ISaga):
  def __init__(self, payment_repository, reward_repository, dispatcher, uow):
    self.payment_repository = payment_repository
    self.reward_repository = reward_repository
    self.dispatcher = dispatcher
    self.uow = uow

  def handle(self, event):
    pass

  def _on_payment_captured(self, event):
    pass