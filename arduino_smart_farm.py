import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QProgressBar, QVBoxLayout, QDialog, QGridLayout, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from PyQt5.QtGui import QColor, QFont
import serial
import time

# 시리얼 통신 객체 생성
ser = serial.Serial("/dev/ttyACM0", 9600)

time.sleep(2)

def get_sensor_values():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="flask_login_demo")
    cursor = connection.cursor()

    cursor.execute("SELECT Temperature, Humidity FROM Dht11_data order by Timestamp desc limit 1")
    temperature_humidity = cursor.fetchone()

    cursor.execute("SELECT Soil_moisture FROM Soil_moisture_data order by Timestamp desc limit 1")
    soil_moisture = cursor.fetchone()

    cursor.execute("SELECT Intensity FROM Light_intensity_data order by Recorded_at desc limit 1"    )
    intensity = cursor.fetchone()

    cursor.close()
    connection.close()

	#ser.write(b'database complete!')

    return temperature_humidity, soil_moisture, intensity

class KeypadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Keypad")
        
        self.layout = QVBoxLayout(self)
        self.line_edit = QLineEdit(self)
        self.layout.addWidget(self.line_edit)

        font = QFont()
        font.setPointSize(20)
        self.line_edit.setFont(font)

        # 키패드 버튼 추가
        self.buttons = []
        grid_layout = QGridLayout()

        button_7 = QPushButton("7", self)
        button_7.clicked.connect(lambda _, digit=7: self.append_digit(digit))
        button_7_font = QFont()
        button_7_font.setPointSize(15)  # 원하는 버튼 텍스트 크기로 설정
        button_7.setFont(button_7_font)
        grid_layout.addWidget(button_7, 0, 0)
        button_width = 50
        button_height = 50
        button_7.setFixedSize(button_width, button_height)

        button_8 = QPushButton("8", self)
        button_8.clicked.connect(lambda _, digit=8: self.append_digit(digit))
        button_8_font = QFont()
        button_8_font.setPointSize(15) 
        button_8.setFont(button_7_font)
        grid_layout.addWidget(button_8, 0, 1)
        button_width = 50
        button_height = 50
        button_8.setFixedSize(button_width, button_height)

        button_9 = QPushButton("9", self)
        button_9.clicked.connect(lambda _, digit=9: self.append_digit(digit))
        button_9_font = QFont()
        button_9_font.setPointSize(15) 
        button_9.setFont(button_7_font)
        grid_layout.addWidget(button_9, 0, 2)
        button_width = 50
        button_height = 50
        button_9.setFixedSize(button_width, button_height)

        button_4 = QPushButton("4", self)
        button_4.clicked.connect(lambda _, digit=4: self.append_digit(digit))
        button_4_font = QFont()
        button_4_font.setPointSize(15) 
        button_4.setFont(button_7_font)
        grid_layout.addWidget(button_4, 1, 0)
        button_width = 50
        button_height = 50
        button_4.setFixedSize(button_width, button_height)

        button_5 = QPushButton("5", self)
        button_5.clicked.connect(lambda _, digit=5: self.append_digit(digit))
        button_5_font = QFont()
        button_5_font.setPointSize(15) 
        button_5.setFont(button_7_font)
        grid_layout.addWidget(button_5, 1, 1)
        button_width = 50
        button_height = 50
        button_5.setFixedSize(button_width, button_height)

        button_6 = QPushButton("6", self)
        button_6.clicked.connect(lambda _, digit=6: self.append_digit(digit))
        button_6_font = QFont()
        button_6_font.setPointSize(15) 
        button_6.setFont(button_7_font)
        grid_layout.addWidget(button_6, 1, 2)
        button_width = 50
        button_height = 50
        button_6.setFixedSize(button_width, button_height)

        button_1 = QPushButton("1", self)
        button_1.clicked.connect(lambda _, digit=1: self.append_digit(digit))
        button_1_font = QFont()
        button_1_font.setPointSize(15) 
        button_1.setFont(button_7_font)
        grid_layout.addWidget(button_1, 2, 0)
        button_width = 50
        button_height = 50
        button_1.setFixedSize(button_width, button_height)

        button_2 = QPushButton("2", self)
        button_2.clicked.connect(lambda _, digit=2: self.append_digit(digit))
        button_2_font = QFont()
        button_2_font.setPointSize(15) 
        button_2.setFont(button_7_font)
        grid_layout.addWidget(button_2, 2, 1)
        button_width = 50
        button_height = 50
        button_2.setFixedSize(button_width, button_height)

        button_3 = QPushButton("3", self)
        button_3.clicked.connect(lambda _, digit=3: self.append_digit(digit))
        button_3_font = QFont()
        button_3_font.setPointSize(15) 
        button_3.setFont(button_7_font)
        grid_layout.addWidget(button_3, 2, 2)
        button_width = 50
        button_height = 50
        button_3.setFixedSize(button_width, button_height)

        button_0 = QPushButton("0", self)
        button_0.clicked.connect(lambda _, digit=0: self.append_digit(digit))
        button_0_font = QFont()
        button_0_font.setPointSize(15) 
        button_0.setFont(button_7_font)
        grid_layout.addWidget(button_0, 3, 0)
        button_width = 50
        button_height = 50
        button_0.setFixedSize(button_width, button_height)

        self.buttons.extend([button_0, button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, button_9])

        # 그리드 레이아웃 내의 위젯들이 차지할 공간의 크기 정책 설정
        grid_layout.setHorizontalSpacing(10)  # 버튼들 간의 가로 간격
        grid_layout.setVerticalSpacing(10)    # 버튼들 간의 세로 간격
        grid_layout.setContentsMargins(10, 10, 10, 10)  # 그리드 레이아웃의 여백

        # 삭제 버튼 추가
        delete_button = QPushButton("삭제", self)
        delete_button.clicked.connect(self.delete_digit)
        delete_button_font = QFont()
        delete_button_font.setPointSize(15) 
        delete_button.setFont(button_7_font)
        grid_layout.addWidget(delete_button, 3, 1)
        button_width = 50
        button_height = 50
        delete_button.setFixedSize(button_width, button_height)

        # 확인 버튼 추가
        confirm_button = QPushButton("입력", self)
        confirm_button.clicked.connect(self.accept)
        confirm_button_font = QFont()
        confirm_button_font.setPointSize(15) 
        confirm_button.setFont(button_7_font)
        grid_layout.addWidget(confirm_button, 3, 2)
        button_width = 50
        button_height = 50
        confirm_button.setFixedSize(button_width, button_height)

        self.layout.addLayout(grid_layout)

    def append_digit(self, digit):
        current_text = self.line_edit.text()
        self.line_edit.setText(current_text + str(digit))

    def delete_digit(self):
        current_text = self.line_edit.text()
        self.line_edit.setText(current_text[:-1])

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi("lcd.ui", self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(2000)

        self.reset_values

        self.app.clicked.connect(self.apply_values)
        self.reset.clicked.connect(self.reset_values)

        self.fan_on.clicked.connect(self.fan_on_button)
        self.fan_off.clicked.connect(self.fan_off_button)

        self.light_on.clicked.connect(self.light_on_button)
        self.light_off.clicked.connect(self.light_off_button)

        self.end.clicked.connect(self.exit_program)

        self.pump_on.clicked.connect(self.pump_on_button)
        self.pump_off.clicked.connect(self.pump_off_button)

        self.layout = QVBoxLayout(self)

        self.temp_value.setPlaceholderText("Click")
        self.temp_value.mousePressEvent = self.open_keypad_temp
        self.layout.addWidget(self.temp_value)

        self.humi_value.setPlaceholderText("Click")
        self.humi_value.mousePressEvent = self.open_keypad_humi
        self.layout.addWidget(self.humi_value)

        self.soil_value.setPlaceholderText("Click")
        self.soil_value.mousePressEvent = self.open_keypad_soil
        self.layout.addWidget(self.soil_value)

        self.light_value.setPlaceholderText("Click")
        self.light_value.mousePressEvent = self.open_keypad_light
        self.layout.addWidget(self.light_value)

    def open_keypad_temp(self, event):
        self.open_keypad(self.temp_value)

    def open_keypad_humi(self, event):
        self.open_keypad(self.humi_value)

    def open_keypad_soil(self, event):
        self.open_keypad(self.soil_value)

    def open_keypad_light(self, event):
        self.open_keypad(self.light_value)

    def open_keypad(self, line_edit):
        keypad_dialog = KeypadDialog(self)
        if keypad_dialog.exec_():
            line_edit.setText(keypad_dialog.line_edit.text())

    def fan_on_button(self):
        self.send_to_arduino(1, 1, "unknown", "unknown")
        self.fan_status.setText("ON")

    def fan_off_button(self):
        self.send_to_arduino(99, 99, "unknown", "unknown")
        self.fan_status.setText("OFF")

    def light_on_button(self):
        self.send_to_arduino("unknown", "unknown", "unknown", 1)
        self.light_status.setText("ON")

    def light_off_button(self):
        self.send_to_arduino("unknown", "unknown", "unknown", 99)
        self.light_status.setText("OFF")

    def pump_on_button(self):
        self.send_to_arduino("unknown", "unknown", 99,"unknown")
        self.pump_status.setText("ON")

    def pump_off_button(self):
        self.send_to_arduino("unknown", "unknown", 1, "unknown")
        self.pump_status.setText("OFF")

    def apply_values(self):
        temp_text = self.temp_value.text()
        temp_value = int(temp_text) if temp_text else 99

        humi_text = self.humi_value.text()
        humi_value = int(humi_text) if humi_text else 99

        soil_text = self.soil_value.text()  
        soil_value = int(soil_text) if soil_text else 1

        light_text = self.light_value.text()
        light_value = int(light_text) if light_text else 99

        self.send_to_arduino(temp_value, humi_value, soil_value, light_value)

    def send_to_arduino(self, temp_value=None, humi_value=None, soil_value=None, light_value=None):
        if temp_value is not None:
            ser.write(str(temp_value).encode())
            ser.write(b',')  # 값들을 구분하기 위한 구분자
        if humi_value is not None:
            ser.write(str(humi_value).encode())
            ser.write(b',')
        if soil_value is not None:
            ser.write(str(soil_value).encode())
            ser.write(b',')
        if light_value is not None:
            ser.write(str(light_value).encode())
        ser.write(b'\n')

    def reset_values(self):
        self.send_to_arduino(99,99,1,99)
        self.temp_value.setText("Click")
        self.humi_value.setText("Click")
        self.soil_value.setText("Click")
        self.light_value.setText("Click")

    def update_data(self):
        temperature_humidity, soil_moisture, intensity = get_sensor_values()
        if temperature_humidity and soil_moisture and intensity:

            temperature, humidity = temperature_humidity

			#print(">>>{}".format(temperature))

            self.temp_bar.setValue(int(temperature))
            self.humi_bar.setValue(int(humidity))
            self.soil_bar.setValue(int(soil_moisture[0]))
            self.light_bar.setValue(int(intensity[0]))

            self.set_temp_bar_color(temperature)
            self.set_humi_bar_color(humidity)
            self.set_soil_bar_color(soil_moisture[0])
            self.set_light_bar_color(intensity[0])

    def set_temp_bar_color(self, value):
        color = self.get_temp_color(value)
        style_sheet = f"QProgressBar::chunk {{ background-color: {color}; }}"
        self.temp_bar.setStyleSheet(style_sheet)

    def set_humi_bar_color(self, value):
        color = self.get_humi_color(value)
        style_sheet = f"QProgressBar::chunk {{ background-color: {color}; }}"
        self.humi_bar.setStyleSheet(style_sheet)

    def set_soil_bar_color(self, value):
        color = self.get_soil_color(value)
        style_sheet = f"QProgressBar::chunk {{ background-color: {color}; }}"
        self.soil_bar.setStyleSheet(style_sheet)

    def set_light_bar_color(self, value):
        color = self.get_light_color(value)
        style_sheet = f"QProgressBar::chunk {{ background-color: {color}; }}"
        self.light_bar.setStyleSheet(style_sheet)

    def get_temp_color(self, value):
        if value > 27:
            return 'red'
        elif value < 18:
            return 'yellow'
        else:
            return 'green'
    def get_humi_color(self, value):
        if value > 75:
            return 'red'
        elif value < 65:
            return 'yellow'
        else:
            return 'green'

    def get_soil_color(self, value):
        if value > 85:
            return 'red'
        elif value < 75:
            return 'yellow'
        else:
            return 'green'

    def get_light_color(self, value):
        if value > 70:
            return 'red'
        elif value < 30:
            return 'yellow'
        else:
            return 'green'

    def exit_program(self):
        sys.exit(0)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    #myWindow.showFullScreen()
    sys.exit(app.exec_())
