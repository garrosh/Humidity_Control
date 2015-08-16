from PyQt5.QtCore import *

class Compressor(QObject):
  ''' A class to hold the compressor and it's associated variables
  '''
  
  updated = pyqtSignal(bool)
  ready = pyqtSignal()
  inactive = pyqtSignal()
  
  
  def __init__(self, parent=None):
    super(Compressor, self).__init__(parent)
    
    self.timer = QTimer(self)
    # Start a timer for 3 minutes, to make sure the compressor is ready to compress before starting it
    self.timer.setSingleShot(True)
    self.timer.setInterval(1800)
    self.timer.start()
    self.timer.timeout.connect(self.set_ready) # Connect the 3 minutes timer to toggle the set_ready slot
    
    self.ready_state = False
    
    self.compressor_state = False # TODO link this variable with an I/O pin
    
    self.waiting_for_start = False
    
    self.updated.emit(self.compressor_state)
 
  def toggle_compressor(self):
    self.set_compressor(self.compressor_state)
    self.updated.emit(self.compressor_state)
    
  def set_compressor(self, state):
    if state:
      start_compressor(self)
    else:
      stop_compressor(self)
    
  def start_compressor(self):
    if ~self.compressor_state:
      if self.ready_state: # Physically start the compressor if possible
        self.compressor_state = True
        self.timer.stop()
        self.timer.timeout.disconnect(self.become_inactive)
        self.timer.start(3600) # Start an hour timer to prevent overheating
        self.timer.timeout.connect(self.react_to_overheat)
        self.updated.emit(self.compressor_state)
      else: # Otherwise, mark for a start ASAP
        self.waiting_for_start = True
      
    
  def stop_compressor(self):
    if self.compressor_state:
      # First deal with the timer, disconnect it from the overheat protection
      self.timer.stop()
      self.timer.timeout.disconnect(self.react_to_overheat)
      # Start the premature restart timer
      self.timer.start(1800)
      self.timer.timeout.connect(self.set_ready)
      self.ready_state = False
      self.compressor_state = False
      self.updated.emit(self.compressor_state)
    elif self.waiting_for_start: # If trying to stop the compressor while waiting_for_start, remove the flag
      self.waiting_for_start = False
    
  def set_ready(self):
    self.ready_state = True
    if self.waiting_for_start:
      self.waiting_for_start = False
      self.start_compressor()
    else: # If the compressor is ready to act, start a timer to trigger an inactive signal
      self.timer.stop()
      self.timer.timeout.disconnect(self.set_ready)
      self.timer.start(3600)
      self.timer.timeout.connect(self.become_inactive)
    self.ready.emit()
  
  def become_inactive(self):
    self.inactive.emit()
    
  def react_to_overheat(self): 
    '''TODO: Add possible overheating behavior here. For now, simply stop and restart
    the compressor '''
  
    self.stop_compressor()
    self.start_compressor()