from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from Controller import Controller

import os, sys, inspect
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
  sys.path.insert(0, cmd_folder)

# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"Icons")))
if cmd_subfolder not in sys.path:
  sys.path.insert(0, cmd_subfolder)

class Form(QMainWindow):
  update_form = pyqtSignal()

  def __init__(self, parent=None):
    super(Form, self).__init__(parent)
    
    self.control = Controller()
    self.control.updated.connect(self.update_form_handle)
    self.control.compressor.updated.connect(self.update_water_icon)
    self.control.heater.updated.connect(self.update_fire_icons)
    
    fibre_saturation_Label = QLabel("Fiber Saturation Ratio (%) (from tables)")
    self.fibre_saturation_spinbox = QDoubleSpinBox()
    self.fibre_saturation_spinbox.setDecimals(1)
    self.fibre_saturation_spinbox.setRange(0, 100)
    self.fibre_saturation_spinbox.setSingleStep(0.1)
    self.fibre_saturation_spinbox.setValue(18)
    self.fibre_saturation_spinbox.valueChanged.connect(self.control.update_EMC_fast_target)
    
    temperature_Label = QLabel("Current temperature measurement")
    self.temperature_value_label = QLabel("{0}".format(self.control.temperature))
    
    humidity_Label = QLabel("Current humidity measurement")
    self.humidity_value_label = QLabel("{0}".format(self.control.humidity))
    
    
    final_saturation_Label = QLabel("Target wood saturation Ratio (%)")
    self.final_saturation_spinbox = QDoubleSpinBox()
    self.final_saturation_spinbox.setDecimals(1)
    self.final_saturation_spinbox.setRange(0, 100)
    self.final_saturation_spinbox.setSingleStep(0.1)
    self.final_saturation_spinbox.setValue(6)
    self.final_saturation_spinbox.valueChanged.connect(self.control.update_EMC_slow_target)
    
    emc_Label = QLabel("Equilibrium Moisture Content")
    self.emc_value_label = QLabel("{0}".format(self.control.equilibrium_moisture_content))
    
    minimum_temperature_Label = QLabel("Minimum operating temperature")
    self.minimum_temperature_spinbox = QDoubleSpinBox()
    self.minimum_temperature_spinbox.setDecimals(1)
    self.minimum_temperature_spinbox.setRange(15,40)
    self.minimum_temperature_spinbox.setSingleStep(0.1)
    self.minimum_temperature_spinbox.setValue(25)
    self.minimum_temperature_spinbox.valueChanged.connect(self.control.heater.set_min)
    
    maximum_temperature_Label = QLabel("Maximum operating temperature")
    self.maximum_temperature_spinbox = QDoubleSpinBox()
    self.maximum_temperature_spinbox.setDecimals(1)
    self.maximum_temperature_spinbox.setRange(15,40)
    self.maximum_temperature_spinbox.setSingleStep(0.1)
    self.maximum_temperature_spinbox.setValue(30)
    self.maximum_temperature_spinbox.valueChanged.connect(self.control.heater.set_max)
    
    self.reset_button = QPushButton("Start new cycle")
    self.reset_button.clicked.connect(self.control.state_starting)
    
    
    self.temp_deque_len_label = QLabel()
    self.temp_deque_len_label.setNum(len(self.control.temp_deque))
    self.dummy_label = QLabel()
    self.dummy_label.setNum(self.control.heater.heating_safe)
    
    
    
    mainLayout = QGridLayout()
    
    '''
    mainLayout.addWidget(fibre_saturation_Label,        0 , 0)
    mainLayout.addWidget(self.fibre_saturation_spinbox, 1 , 0)
    mainLayout.addWidget(temperature_Label,             2 , 0)
    mainLayout.addWidget(self.temperature_value_label,  3 , 0)
    mainLayout.addWidget(humidity_Label,                4 , 0)
    mainLayout.addWidget(self.humidity_value_label,     5 , 0)
    
    
    mainLayout.addWidget(final_saturation_Label,        0 , 1)
    mainLayout.addWidget(self.final_saturation_spinbox, 1 , 1)
    mainLayout.addWidget(emc_Label,                     2 , 1)
    mainLayout.addWidget(self.emc_value_label,          3 , 1)
    mainLayout.addWidget(self.temp_deque_len_label,     4 , 1)
    mainLayout.addWidget(self.dummy_label,              5 , 1)
    '''
    mainLayout.addWidget(fibre_saturation_Label,           0 , 0)
    mainLayout.addWidget(self.fibre_saturation_spinbox,    1 , 0)
    mainLayout.addWidget(final_saturation_Label,           2 , 0)
    mainLayout.addWidget(self.final_saturation_spinbox,    3 , 0)
    
    mainLayout.addWidget(humidity_Label,                   0 , 1)
    mainLayout.addWidget(self.humidity_value_label,        1 , 1)
    mainLayout.addWidget(temperature_Label,                2 , 1)
    mainLayout.addWidget(self.temperature_value_label,     3 , 1)
    mainLayout.addWidget(self.reset_button,                4 , 1)
    
    mainLayout.addWidget(minimum_temperature_Label,        0 , 2)
    mainLayout.addWidget(self.minimum_temperature_spinbox, 1 , 2) 
    mainLayout.addWidget(maximum_temperature_Label,        2 , 2)
    mainLayout.addWidget(self.maximum_temperature_spinbox, 3 , 2)
    
    self.fire_icon   = QPixmap("burn.png")
    self.red_icon    = QPixmap("circle_red.png")
    self.green_icon  = QPixmap("circle_green.png")
    self.fire_label1 = QLabel()
    self.fire_label2 = QLabel()
    self.fire_label1.setPixmap(self.fire_icon)
    self.fire_label2.setPixmap(self.fire_icon)
    
    self.water_icon  = QPixmap("water.png")
    self.water_label = QLabel()
    self.water_label.setPixmap(self.water_icon)
    
    self.statusBar = QStatusBar()
    self.statusBar.addPermanentWidget(self.fire_label1)
    self.statusBar.addPermanentWidget(self.fire_label2)
    self.statusBar.addPermanentWidget(self.water_label)
    self.statusBar.showMessage("{0} - {1} - {2}".format(self.control.state,self.control.states_list[self.control.state],len(self.control.temp_deque)))
    
    
   
    
    centralWidget = QWidget()
    centralWidget.setLayout(mainLayout)
    
    self.setCentralWidget(centralWidget)
    self.setWindowTitle("Humidity Control V1.0")
    self.setStatusBar(self.statusBar)
    
    self.control.compressor.updated.emit()
    self.control.heater.updated.emit()

    


  def update_form_handle(self):
    
    self.temperature_value_label.setNum(self.control.temperature)
    self.humidity_value_label.setNum(self.control.humidity)
    self.emc_value_label.setNum(self.control.equilibrium_moisture_content)
    self.temp_deque_len_label.setNum(len(self.control.temp_deque))
    self.dummy_label.setNum(self.control.heater.heating_safe)
    self.statusBar.showMessage("{0} - {1} - {2}".format(self.control.state,self.control.states_list[self.control.state],len(self.control.temp_deque)))
    
  def update_water_icon(self):
    if self.control.compressor.compressor_state:
      self.water_label.setPixmap(self.water_icon)
    elif self.control.compressor.ready_state:
      self.water_label.setPixmap(self.green_icon)
    else:
      self.water_label.setPixmap(self.red_icon)
      
  def update_fire_icons(self):
    if self.control.heater.heater1:
      self.fire_label1.setPixmap(self.fire_icon)
    else:
      self.fire_label1.setPixmap(self.red_icon)
    if self.control.heater.heater2:
      self.fire_label2.setPixmap(self.fire_icon)
    else:
      self.fire_label2.setPixmap(self.red_icon)


if __name__ == '__main__':
  import sys
  
  app = QApplication(sys.argv)
  
  screen = Form()
  screen.show()
  
  sys.exit(app.exec_())
