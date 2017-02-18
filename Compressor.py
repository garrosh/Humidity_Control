from PyQt5.QtCore import *
import RPi.GPIO as GPIO

class Compressor(QObject):
  ''' A class to hold the compressor and it's associated variables
  '''
  
  updated   = pyqtSignal()
  is_active = pyqtSignal(bool)
  is_idle   = pyqtSignal()
  
  
  def __init__(self, parent=None):
    super(Compressor, self).__init__(parent)

    GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
    
        
    self.ready_state = False  # Internal value to track if the compressor is ready

    self.idle_state = False # Inernal value to track if the compressor is idle
    
    self.compressor_state = False # TODO link this variable with an I/O pin
    
    self.waiting_for_start = False # Internal value to track if the compressor is waiting to start

    # Counter to use to check time since last compressor command
    self.timer_counter = 0

  def counter_tick(self):
    self.timer_counter += 1
    # If the compressor is idle, roll back the counter
    if self.idle_state:
      self.timer_counter = 0

    # Check if the counter is high enough to fire to make the compressor ready
    if (not self.ready_state) and self.timer_counter > 18 and (not self.idle_state):
      self.timer_counter = 0
      self.set_ready()
    # Check if the counter is high enough to make the compressor idle
    if self.ready_state and self.timer_counter > 36 and (not self.idle_state):
      self.timer_counter = 0
      self.idle_state = True
      self.is_idle.emit()
    # Check if the counter is high enough to make it shutdown from overheating
    if self.compressor_state and self.timer_counter > 36:
      self.timer_counter = 0
      self.react_to_overheat()

      
  
  def toggle_compressor(self):
    self.set_compressor(not self.compressor_state)
    
  def set_compressor(self, state):
    if state:
      self.start_compressor(self)
      GPIO.output(15, GPIO.LOW)
    else:
      self.stop_compressor(self)
      GPIO.output(15, GPIO.HIGH)
    
  def start_compressor(self):
    if not self.compressor_state:
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
      self.updated.emit()
  
  def become_inactive(self):
    if self.compressor_state:
      self.ready_state = False
      self.compressor_state = False
      self.is_active.emit(self.get_state())
      self.updated.emit()
    
  def become_active(self):
    if not self.compressor_state:
      self.compressor_state = True
      self.idle_state = False
      self.is_active.emit(self.get_state())
      self.updated.emit()
    
  def get_state(self):
    if self.compressor_state:
      return 1
    else:
      return 0
    
  def react_to_overheat(self): 
    '''TODO: Add possible overheating behavior here. For now, simply stop and restart
    the compressor '''
  
    self.stop_compressor()
    self.start_compressor()
