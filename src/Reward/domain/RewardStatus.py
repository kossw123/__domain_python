from enum import Enum

class RewardStatus(Enum):
  PENDING = 0
  GRANTED = 1
  USED = 2
  EXPIRED = 3