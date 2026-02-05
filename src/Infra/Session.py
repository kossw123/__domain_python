class Session():
  def __init__(self):
    self.actions = []

  def add(self, action):
    self.actions.append(action)

  def commit(self):
    print("COMMIT:", self.actions)

  def rollback(self):
    print("ROLLBACK")
    self.actions.clear()
