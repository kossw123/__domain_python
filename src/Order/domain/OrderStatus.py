from enum import Enum
class OrderStatus(Enum):
  CREATE = 0            # 주문 생성됨
  PAID = 2              # 결제 완료
  SHIPPED = 3           # 배송 중
  PENDINGPAYMENT = 1    # 결제 대기
  COMPLETED = 4         # 거래 완료
  CANCELLED = 5         # 주문 취소