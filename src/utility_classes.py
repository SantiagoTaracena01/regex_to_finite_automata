class State(object):

  def __init__(self, state):
    self.__state = state
    self.__label = None
    self.__first_edge = None
    self.__last_edge = None

  def get_state(self):
    return self.__state

  def set_state(self, state):
    self.__state = state

  def get_label(self):
    return self.__label

  def set_label(self, label):
    self.__label = label

  def get_first_edge(self):
    return self.__first_edge

  def set_first_edge(self, first_edge):
    self.__first_edge = first_edge

  def get_last_edge(self):
    return self.__last_edge

  def set_last_edge(self, last_edge):
    self.__last_edge = last_edge

  def __repr__(self):
    return str(self.__state)

class SimpleNFA(object):

  def __init__(self, generated_by, initial_state, acceptance_states):
    self.__generated_by = generated_by
    self.__initial_state = initial_state
    self.__acceptance_states = acceptance_states

  def get_generated_by(self):
    return self.__generated_by

  def get_initial_state(self):
    return self.__initial_state

  def set_initial_state(self, initial_state):
    self.__initial_state = initial_state

  def get_acceptance_states(self):
    return self.__acceptance_states

  def set_acceptance_states(self, acceptance_states):
    self.__acceptance_states = acceptance_states
