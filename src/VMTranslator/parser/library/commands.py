

class Commands():
  def __init__(self):
    self.arithmetic_logic = set(['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'])
    self.non_logic = set(['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL'])