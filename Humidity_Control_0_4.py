from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Controller import Controller

class Form(QWidget):
  update_form = pyqtSignal()

  def __init__(self, parent=None):
    super(Form, self).__init__(parent)
    
    self.control = Controller()
    
    fibre_saturation_Label = QLabel("Fiber Saturation Ratio (%) (from tables)")
    self.fibre_saturation_spinbox = QDoubleSpinBox()
    self.fibre_saturation_spinbox.setDecimals(1)
    self.fibre_saturation_spinbox.setRange(0, 100)
    self.fibre_saturation_spinbox.setSingleStep(0.1)
    self.fibre_saturation_spinbox.setValue(18)
    
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
    
    emc_Label = QLabel("Equilibrium Moisture Content")
    self.emc_value_label = QLabel("{0}".format(self.control.equilibrium_moisture_content))
    
    self.temp_deque_len_label = QLabel()
    self.temp_deque_len_label.setNum(len(self.control.temp_deque1))
    self.dummy_label = QLabel()
    self.dummy_label.setNum(self.control.state)
    
    
    
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
    mainLayout.addWidget(self.temp_deque_len_label,     4 , 1)
    mainLayout.addWidget(self.dummy_label,              5 , 1)
    
    
    
    
    self.setLayout(mainLayout)
    self.setWindowTitle("Humidity Control V0.4")
    

    self.control.updated.connect(self.update_form_handle)


  def update_form_handle(self):
    
    self.temperature_value_label.setNum(self.control.temperature)
    self.humidity_value_label.setNum(self.control.humidity)
    self.emc_value_label.setNum(self.control.equilibrium_moisture_content)
    self.temp_deque_len_label.setNum(len(self.control.temp_deque1))
    self.dummy_label.setNum(self.control.state)


if __name__ == '__main__':
  import sys
  
  app = QApplication(sys.argv)
  
  screen = Form()
  screen.show()
  
  sys.exit(app.exec_())
