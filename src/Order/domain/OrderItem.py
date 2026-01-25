
class OrderItem():
  def __init__(self, product_id, price, quantity):
    self.product_id = product_id
    self.price = price
    self.quantity = quantity
  @classmethod
  def create(cls, product_id, price, quantity):
    return cls(product_id, price, quantity)
  def total(self):
    return self.price * self.quantity
  def __str__(self):
    return f"OrderItems(product_id={self.product_id}, price={self.price}, quantity={self.quantity})"