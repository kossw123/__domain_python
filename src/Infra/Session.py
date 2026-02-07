class Session():
  def __init__(self):
    self.actions = []

  def add(self, action):
    self.actions.append(action)

  def commit(self):
    #print("COMMIT:", self.actions)
    print("[UOW] COMMIT")

  def rollback(self):
    print("[UOW] ROLLBACK")
    self.actions.clear()
