from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from calc_EMC import calc_EMC

class Form(QWidget):
  def __init__(self, parent=None):
    super(Form, self).__init__(parent)
    
    self.temperature = 140
    self.humidity = 0.55
    
    fibre_saturation_Label = QLabel("Fiber Saturation Ratio (%) (from tables)")
    self.fibre_saturation_spinbox = QDoubleSpinBox()
    self.fibre_saturation_spinbox.setDecimals(1)
    self.fibre_saturation_spinbox.setRange(0, 100)
    self.fibre_saturation_spinbox.setSingleStep(0.1)
    self.fibre_saturation_spinbox.setValue(18)
    
    temperature_Label = QLabel("Current temperature measurement")
    temperature_value_label = QLabel("{0}".format(self.temperature))
    
    humidity_Label = QLabel("Current humidity measurement")
    humidity_value_label = QLabel("{0}".format(self.humidity))
    
    
    final_saturation_Label = QLabel("Target wood saturation Ratio (%)")
    self.final_saturation_spinbox = QDoubleSpinBox()
    self.final_saturation_spinbox.setDecimals(1)
    self.final_saturation_spinbox.setRange(0, 100)
    self.final_saturation_spinbox.setSingleStep(0.1)
    self.final_saturation_spinbox.setValue(6)
    
    
    
    
    
    mainLayout = QGridLayout()
    
    
    mainLayout.addWidget(fibre_saturation_Label,        0 , 0)
    mainLayout.addWidget(self.fibre_saturation_spinbox, 1 , 0)
    mainLayout.addWidget(temperature_Label,             2 , 0)
    mainLayout.addWidget(temperature_value_label,       3 , 0)
    mainLayout.addWidget(humidity_Label,                4 , 0)
    mainLayout.addWidget(humidity_value_label,          5 , 0)
    
    
    mainLayout.addWidget(final_saturation_Label,        0 , 1)
    mainLayout.addWidget(self.final_saturation_spinbox, 1 , 1)
    
    
    
    
    self.setLayout(mainLayout)
    self.setWindowTitle("Humidity Control V0.2")
      
  def submitContact(self):
    name = self.nameLine.text()
    
    if name == "":
      QMessageBox.information(self, "Empty Field", "Please enter a name and address.")
    else:
      new_EMC = calc_EMC(140, 0.55)
      QMessageBox.information(self, "Success!", "Hello {0}! You calculated {1}".format(name, new_EMC))
      
if __name__ == '__main__':
  import sys
  
  app = QApplication(sys.argv)
  
  screen = Form()
  screen.show()
  
  sys.exit(app.exec_())

for ii in range(0,200):
  print(calc_EMC(ii,0.50))
