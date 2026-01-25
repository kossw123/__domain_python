from src.Product.domain.ProductStatus import ProductStatus
from src.Infra.AggregateRoot import AggregateRoot
from src.Product.domain.events import *


class Product():
  def __init__(self, product_id, name, price, stock):
    self.aggregate_root = AggregateRoot()
    self.id = product_id
    self.name = name
    self.price = price
    self.stock = stock
    self.status = ProductStatus.DRAFT

  @classmethod
  def create(cls, id, name, price, stock):
    if not name:
      raise Exception("name is required")
    if not price:
      raise Exception("price is required")

    product = cls(id, name, price, stock)
    product.aggregate_root.register(
        ProductCreated(
            product.id,
            product.name,
            product.price))
    return product

  def activate(self):           # 판매 시작
    if self.status == ProductStatus.ACTIVE:
      return
    if self.status == ProductStatus.OUTOFSTOCK:
      raise Exception("OUTOFSTOCK")
    if self.status == ProductStatus.DISCONTINUED:
      raise Exception("DISCONTINUED")
    self.status = ProductStatus.ACTIVE
    self.aggregate_root.register(ProductActivated(self.id, self.name))

  def decrease_stock(self, quantity):     # 재고 차감
    if self.stock <= 0:
      self.status ==  ProductStatus.OUTOFSTOCK
      raise Exception("OUTOFSTOCK")
    self.stock -= quantity
    self.aggregate_root.register(ProductStockDecreased(self.id, self.name, self.stock))
  def increase_stock(self, quantity):     # 재고 증가
    if self.status == ProductStatus.DISCONTINUED:
      raise Exception("DISCONTINUED")
    self.stock += quantity
    self.aggregate_root.register(ProductStockIncreased(self.id, self.name, self.stock))
  def discontinued(self):       # 판매 종료
    if self.status == ProductStatus.DISCONTINUED:
      return;
    self.status = ProductStatus.DISCONTINUED
    self.aggregate_root.register(ProductDiscontinued(self.id, self.name))
  def __str__(self):
    return f"Product(id={self.id}, name={self.name}, stock={self.stock}, status={self.status.name})"