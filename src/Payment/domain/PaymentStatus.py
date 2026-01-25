from enum import Enum

class PaymentStatus(Enum):
  INITIALIZED = 0
  AUTHORIZED = 1
  CAPTURED = 2
  FAILED = 3
  REFUNCED = 4