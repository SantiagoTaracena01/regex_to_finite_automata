class Stack(object):

  def __init__(self, initial_values=[]):
    self.__stack = initial_values

  def __len__(self):
    return len(self.__stack)

  def __str__(self):
    return str(self.__stack)

  def is_empty(self):
    return (len(self.__stack) == 0)

  def push(self, item):
    self.__stack.append(item)

  def peek(self):
    return (self.__stack[-1] if (not self.is_empty()) else "")

  def pop(self):
    last_element = self.__stack[-1]
    self.__stack.remove(last_element)
    return last_element

  # def get_index(self, value):
  #   for index, element in enumerate(self.__stack):
  #     if (element == value):
  #       return index
  #   return -1

  # def contains(self, value):
  #   return (value in self.__stack)

  # def get(self, index):
  #   return self.__stack[index]
