from PyQt5.QtCore import *
from calc_EMC import calc_EMC
from collections import deque
from statistics import mean
from Compressor import Compressor
from Heater import Heater
import random

import RPi.GPIO as GPIO
import smbus
import time


class Controller(QObject):
  ''' Humidity controller class
  
  This class is a self contained container which tries to stabilize the
  Equilibrium Moisture Content of the wood by using the Hailwood-Horrobin equation
  (see calc_EMC.py for details)
  
  Drying is done in two stages. In the first stage, while the wood is green, the controller
  attempts to keep the air at the requested EMC without interruption. Once the controller
  notices it hasn't dried for a long (TODO: Determine interval) time, it moves to the second stage,
  where it tries to bring the air to the specified EMC for a while (TODO: Determine interval) and
  then lets the wood balance itself for an other while (TODO: Determine interval). When the controller
  notices that balancing doesn't influence ambiant humidity, the wood is considered dried.
  
  '''
 
  updated = pyqtSignal()

  def __init__(self, parent=None):
    super(Controller, self).__init__(parent)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    self.bus = smbus.SMBus(1)
    self.address = 0x27

    

    # Temperature1 pin #: 17
    # Temperature2 pin #: 27
    # Compressor   pin #: 22
    
    
    # temperature1 = 20 # TODO Read temperature sensor here
    # temperature2 = 20 # TODO Read temperature sensor here
    # humidity1 = 0.55 # TODO Read humidity sensor here
    # humidity2 = 0.55 # TODO Read humidyty sensor here
    
    # self.temperature = (temperature1 + temperature2) / 2
    # self.humidity = (humidity1 + humidity2) /2
    
    self.heater = Heater()
    
    self.compressor = Compressor()
    
    self.compressor.is_active.connect(self.heater.set_heating_safe)
    
    # self.temp_deque1 = deque([],180)
    # self.temp_deque2 = deque([],180)
    
    self.temp_deque = deque([],180)
    
    self.states_list = ['starting','fast_drying','slow_drying','standby','failure']
    
    self.state = 0

    self.complete_sensor_read()
    self.equilibrium_moisture_content = calc_EMC(self.temperature,self.humidity)
    
    self.EMC_fast_target = 18.0
    self.EMC_fast_error = 2.0
    self.EMC_slow_target = 6.0
    self.EMC_slow_error = 1.0
    
    self.timer = QTimer(self)
    self.timer.setSingleShot(False)
    self.timer.timeout.connect(self.dispatch_state(self.states_list[self.state]))
    self.timer.timeout.connect(self.complete_sensor_read)
    self.timer.timeout.connect(self.compressor.counter_tick)
    
    self.timer.start(100)
    

  def request_sensor_read(self):
    self.bus.write_byte(self.address, 0)

  def process_sensor_read(self):
    buf = self.bus.read_i2c_block_data(self.address,0,4)
    '''print(repr(buf[0]).rjust(4),repr(buf[1]).rjust(4),repr(buf[2]).rjust(4),repr(buf[3]).rjust(4))'''
    status = (buf[0] & 0xc0) >> 6
    self.humidity = (((buf[0] & 0x3f) *256) + buf[1]) / 0x3fff * 100
    temperature = (buf[2] *256 + buf[3]) / 0xfffc * 165 - 40
    self.temp_deque.append(temperature)
    self.temperature = mean(self.temp_deque)
    self.update_EMC_handle()


  def complete_sensor_read(self):
    self.request_sensor_read()
    time.sleep(0.0)
    self.process_sensor_read()
    
  def update_EMC_handle(self):
    ''' This function simply recalculates EMC based on internal values, and then
    emits an updated signal 
    '''
    self.equilibrium_moisture_content = calc_EMC(self.temperature, self.humidity)
    
    self.updated.emit()
    
  def update_EMC_fast_target(self, new_target):
    self.EMC_fast_target = new_target
    
  def update_EMC_slow_target(self, new_target):
    self.EMC_slow_target = new_target
    
    
  def state_starting(self):
    ''' A state function meant to fill the deques and avoid starting bumps '''
    
    self.state = 0
    if len(self.temp_deque) == 18:
      self.check_starting()
     
    
  def check_starting(self):
    self.heater.half_heating = False
    try:
      self.timer.timeout.disconnect(self.dispatch_state(self.states_list[self.state]))
      self.timer.timeout.connect(self.state_fast_drying)
    except:
      pass
    # Completely reset internal values of compressor, if sent from an other state
    if self.state != 0:
      self.compressor.idle_state = False
      self.compressor.waiting_for_start = False
      self.compressor.timer_counter = 0
      self.compressor.ready_state = False
      self.compressor.compressor_state = False
      self.compressor.is_active.emit(self.compressor.get_state())
      self.compressor.updated.emit()
    self.state = 1
      
  def state_fast_drying(self):
    ''' While fast drying, heat as much up to 60 C and keep EMC at target plus or minus 2% 
    The compressor kicks in if the EMC becomes too high, and stops if it becomes too low'''
    self.state = 1
    self.heater.update_heating(self.temperature)

    # Validate compressor status relative to EMC
    if self.equilibrium_moisture_content - self.EMC_fast_error > self.EMC_fast_target:
      self.compressor.start_compressor()
    elif self.equilibrium_moisture_content + self.EMC_fast_error < self.EMC_fast_target:
      self.compressor.stop_compressor()

    if self.compressor.idle_state:
      self.check_fast_drying()
      
  def check_fast_drying(self):
    ''' If the compressor becomes inactive while fast drying, we are ready for slow drying '''
    
    # Change the connection with the disconnect signal
    self.timer.timeout.disconnect(self.dispatch_state(self.states_list[self.state]))
    self.state = 2
    self.timer.timeout.connect(self.state_slow_drying)
    # Make sure to set only one heater before slow drying
    self.heater.half_heating = True
    self.compressor.start_compressor()
      
  def state_slow_drying(self):
    ''' While slow drying, heat with only 1 element up to 40 C and drops EMC at target minus 1%, then waits
    until checking for a restart'''
    self.state = 2
    self.heater.update_heating(self.temperature)
    
    if self.equilibrium_moisture_content + self.EMC_slow_error < self.EMC_slow_target:
      self.compressor.stop_compressor()

    if self.compressor.idle_state:
      self.check_slow_drying()
    
  def check_slow_drying(self):
    ''' When the compressor becomes inactive while slow drying, check if it needs to be started again.
    If it doesn't need to start, the wood is dry. '''
    if self.equilibrium_moisture_content - self.EMC_slow_error / 2 > self.EMC_slow_target:
      self.compressor.start_compressor()
    else:
      self.timer.timeout.disconnect(self.dispatch_state(self.states_list[self.state]))
      self.state = 3
      self.timer.timeout.connect(self.state_standby)
      self.heater.half_heating = False
      self.heater.set_heaters(False, False)

    
   
  def state_standby(self):
    pass
    
  def check_standby(self):
    pass
   
  def set_EMC_fast_target(self, fast_target):
    self.EMC_fast_target = fast_target
    
  def set_EMC_slow_target(self, slow_target):
    self.EMC_slow_target = slow_target

    
  def dispatch_state(self, value):
    ''' Return the method name based on the state '''
    method_name = 'state_' + str(value)
    return getattr(self, method_name)
