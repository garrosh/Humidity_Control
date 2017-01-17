from PyQt5.QtCore import *

class Compressor(QObject):
  ''' A class to hold the compressor and it's associated variables
  '''
  
  updated   = pyqtSignal()
  is_active = pyqtSignal(bool)
  is_idle   = pyqtSignal()
  
  
  def __init__(self, parent=None):
    super(Compressor, self).__init__(parent)
    
    self.timer = QTimer(self)
    # Start a timer for 3 minutes, to make sure the compressor is ready to compress before starting it
    self.timer.setSingleShot(True)
    self.timer.setInterval(1800)
    self.timer.start()
    self.timer.timeout.connect(self.set_ready) # Connect the 3 minutes timer to toggle the set_ready slot
    
    self.ready_state = False  # Internal value to track if the compressor is due to start
    
    self.compressor_state = False # TODO link this variable with an I/O pin
    
    self.waiting_for_start = False
 
  def toggle_compressor(self):
    self.set_compressor(~self.compressor_state)
    
  def set_compressor(self, state):
    if state:
      self.start_compressor(self)
    else:
      self.stop_compressor(self)
    
  def start_compressor(self):
    if ~self.compressor_state:
      if self.ready_state: # Physically start the compressor if possible
        self.become_active()
        # TODO: Put code to include overheat prevention?
      else: # Otherwise, mark for a start ASAP
        self.waiting_for_start = True
      
    
  def stop_compressor(self):
    if self.compressor_state:
      self.become_inactive()
    elif self.waiting_for_start: # If trying to stop the compressor while waiting_for_start, remove the flag
      self.waiting_for_start = False
    
  def set_ready(self):
    self.ready_state = True
    if self.waiting_for_start:
      self.waiting_for_start = False
      self.start_compressor()
    else: # If the compressor is ready to act, start a timer to trigger an inactive signal
      self.timer.stop()
      self.timer.timeout.disconnect()
      self.timer.start(3600)
      self.timer.timeout.connect(self.is_idle)
      self.updated.emit()
  
  def become_inactive(self):
    if self.compressor_state:
      # First deal with the timer, disconnect it from the overheat protection
      self.timer.stop()
      self.timer.timeout.disconnect()
      # Start the premature restart timer
      self.timer.start(1800)
      self.timer.timeout.connect(self.set_ready)
      self.ready_state = False
      
      self.compressor_state = False
      self.is_active.emit(self.compressor_state)
      self.updated.emit()
    
  def become_active(self):
    if ~self.compressor_state:
      self.timer.stop()
      self.timer.timeout.disconnect()
      self.timer.start(6000) # Start a one hour timer to time overheat
      self.timer.timeout.connect(self.react_to_overheat)
      self.compressor_state = True
      self.is_active.emit(self.compressor_state)
      self.updated.emit()
    
  def get_state(self):
    return self.compressor_state
    
  def react_to_overheat(self): 
    '''TODO: Add possible overheating behavior here. For now, simply stop and restart
    the compressor '''
  
    self.stop_compressor()
    self.start_compressor()
