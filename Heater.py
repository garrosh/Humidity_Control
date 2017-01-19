from PyQt5.QtCore import *

class Heater(QObject):
  ''' A class to hold the heater and it's associated variables
  '''
  
  updated = pyqtSignal()
  
  def __init__(self, parent=None):
    super(Heater, self).__init__(parent)
    
    self.heater1 = False
    self.heater2 = False
    self.heating_safe = False
    self.minimum = 0
    self.maximum = 0
    self.half_heating = False
    self.half_heating_lock = False
    self.timer = QTimer(self)
    self.timer.setInterval(6000)
    self.timer.timeout.connect(self.toggle_heaters)
    
  def set_min_max(self, minimum, maximum):
    self.minimum = minimum
    self.maximum = maximum
    
  def update_heating(self,temperature):
    if self.heating_safe:
      if self.maximum < temperature:
        self.set_heaters(False, False)
        if self.half_heating:
          self.timer.stop()
      elif self.minimum > temperature:
        if self.half_heating:
          if ~self.half_heating_lock:
            self.timer.start()
            self.half_heating_lock = True
            self.set_heaters(True, False)
        else:
          self.set_heaters(True,True)
    else:
      self.set_heaters(False,False)
      
  
  def toggle_heaters(self):
    if self.heating_safe:
      self.set_heaters(~self.heater1, ~self.heater2)
    else:
      self.set_heaters(False,False)
    
  
  def set_heaters(self, state_heater1, state_heater2):
    if self.heating_safe:
      self.heater1 = state_heater1
      self.heater2 = state_heater2
    else:
      self.heater1 = False
      self.heater2 = False
    self.updated.emit()
  
  
  @pyqtSlot(bool)
  def set_heating_safe(self, compressor_active):
    if compressor_active:
      self.heating_safe = False
    else:
      self.heating_safe = True
  
  def get_heater1(self):
    return self.heater1
    
  def get_heater2(self):
    return self.heater2
