from PyQt5.QtCore import *

class Heater(QObject):
  ''' A class to hold the heater and it's associated variables
  '''
  
  
  def __init__(self, parent=None):
    super(Heater, self).__init__(parent)
    
    self.heater1 = False
    self.heater2 = False
    self.minimum = 0
    self.maximum = 0
    self.half_heating = False
    self.heater1_was_last = False
    self.timer = QTimer(self)
    self.timer.setInterval(600000)
    self.timer.timeout.connect(self.toggle_heaters)
    
  def set_min_max(self, minimum, maximum):
    self.minimum = minimum
    self.maximum = maximum
    
  def update_heating(self,temperature):
    if self.maximum > temperature:
      self.heater1 = False
      self.heater2 = False
      if self.half_heating:
        self.timer.stop()
    elif self.minimum < temperature:
      if self.half_heating:
        self.start_half_heat()
      else:
        self.set_heaters(True,True)
  
  def start_half_heat(self):
    if self.heater1_was_last:
      self.set_heaters(False,True)
      self.heater1_was_last = False
    else:
      self.set_heaters(True, False)
      self.heater1_was_last = True
    self.timer.start()
  
  def toggle_heaters(self):
    self.set_heaters(~self.heater1, ~self.heater2)
  
  def set_heaters(self, state_heater1, state_heater2):
    self.heater1 = state_heater1
    self.heater2 = state_heater2