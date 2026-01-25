
class Repository:
  def __init__(self):
    self.store = {}
  def save(self, obj):
    self.store[obj.id] = obj
  def find(self, id):
    return self.store.get(id)
  def delete(self, id):
    del self.store[id]

  def find_by_order_id(self, order_id):
    for payment in self.store.values():
      if payment.order_id == order_id:
        return payment
    return None

  def __len__(self):
    return len(self.store)
  def __str__(self):
    if not self.store:
      return "Repository(empty)"

    lines = ["Repository:"]
    for k, v in self.store.items():
      lines.append(f"  - {k}: {v}")
    return "\n".join(lines)

  def __repr__(self):
    return f"<Repository size={len(self.store)}>"
