from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from calc_EMC import calc_EMC
import random

class Form(QWidget):
  # Define a new signal called 'trigger' that has no arguments.
  update_EMC = pyqtSignal()

  def __init__(self, parent=None):
    super(Form, self).__init__(parent)
    
    self.temperature = 140
    self.humidity = 0.55
    
    self.equilibrium_moisture_content = calc_EMC(self.temperature,self.humidity)
    
    fibre_saturation_Label = QLabel("Fiber Saturation Ratio (%) (from tables)")
    self.fibre_saturation_spinbox = QDoubleSpinBox()
    self.fibre_saturation_spinbox.setDecimals(1)
    self.fibre_saturation_spinbox.setRange(0, 100)
    self.fibre_saturation_spinbox.setSingleStep(0.1)
    self.fibre_saturation_spinbox.setValue(18)
    
    temperature_Label = QLabel("Current temperature measurement")
    self.temperature_value_label = QLabel("{0}".format(self.temperature))
    
    humidity_Label = QLabel("Current humidity measurement")
    self.humidity_value_label = QLabel("{0}".format(self.humidity))
    
    
    final_saturation_Label = QLabel("Target wood saturation Ratio (%)")
    self.final_saturation_spinbox = QDoubleSpinBox()
    self.final_saturation_spinbox.setDecimals(1)
    self.final_saturation_spinbox.setRange(0, 100)
    self.final_saturation_spinbox.setSingleStep(0.1)
    self.final_saturation_spinbox.setValue(6)
    
    emc_Label = QLabel("Equilibrium Moisture Content")
    self.emc_value_label = QLabel("{0}".format(self.equilibrium_moisture_content))
    
    
    
    mainLayout = QGridLayout()
    
    
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
    
    
    
    
    self.setLayout(mainLayout)
    self.setWindowTitle("Humidity Control V0.3")
    
    
    #def connect_and_emit_trigger(self):
    # Connect the trigger signal to a slot.
    self.update_EMC.connect(self.update_EMC_handle)

    # Emit the signal.
    self.update_EMC.emit()

    
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.random_noise)
    self.timer.start(1000)

  def update_EMC_handle(self):
    
    self.equilibrium_moisture_content = calc_EMC(self.temperature, self.humidity)
    self.temperature_value_label.setNum(self.temperature)
    self.humidity_value_label.setNum(self.humidity)
    self.emc_value_label.setNum(self.equilibrium_moisture_content)

  def random_noise(self):
    self.temperature = self.temperature + random.uniform(-0.45,0.55)
    self.humidity    = self.humidity    + random.uniform(-0.1 , 0.1)
    self.update_EMC.emit()

if __name__ == '__main__':
  import sys
  
  app = QApplication(sys.argv)
  
  screen = Form()
  screen.show()
  
  sys.exit(app.exec_())
