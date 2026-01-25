

class RewardService():
  def __init__(self, reward_repository, dispatcher, uow):
    self.reward_repository = reward_repository
    self.dispatcher = dispatcher
    self.uow = uow

  def grant(self, id):
    reward = self.reward_repository.find(id)
    reward.grant()
    self.reward_repository.save(reward)
    self.__register_uow_to_dispatch(reward)
  def use(self, id):
    reward = self.reward_repository.find(id)
    reward.use()
    self.reward_repository.save(reward)
    self.__register_uow_to_dispatch(reward)
  def expire(self, id):
    reward = self.reward_repository.find(id)
    reward.expire()
    self.reward_repository.save(reward)
    self.__register_uow_to_dispatch(reward)


  def __register_uow_to_dispatch(self, obj):
    self.uow.register(obj)
    while True:
      events = self.uow.collect_events()
      if not events:
        break
      self.dispatcher.dispatch(events)