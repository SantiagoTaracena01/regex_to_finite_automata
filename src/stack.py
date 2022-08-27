class Stack(object):

  def __init__(self, initial_values=[]):
    self.__stack: list = initial_values

  def push(self, value=None):
    if value is not None:
      self.__stack.append(value)
    else:
      raise Exception("Must push a valid value.")

  def peek(self):
    try:
      return self.__stack[-1]
    except:
      raise Exception("Must have inserted values before.")

  def pop(self):
    element = self.peek()
    self.__stack.remove(element)
    return element

  def length(self):
    return len(self.__stack)

  def empty(self):
    return (self.__stack.__len__() == 0)

  def __str__(self):
    return str(self.__stack)
