from enum import Enum
class ProductStatus(Enum):
  DRAFT = 0             # 생성되었지만 판매 불가
  ACTIVE = 1            # 판매 불가
  OUTOFSTOCK = 2        # 재고 0
  DISCONTINUED = 3      # 판매 종료