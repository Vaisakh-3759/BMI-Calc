import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt

connect = sqlite3.connect('bmi_data.db')
c = connect.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_entries
             (id INTEGER PRIMARY KEY, weight REAL, height REAL, bmi REAL, date TEXT)''')
connect.commit()

class BMI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMI Calculator")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.weight_label = QLabel("Weight (kg):")
        layout.addWidget(self.weight_label)
        self.weight_entry = QLineEdit()
        layout.addWidget(self.weight_entry)

        self.height_label = QLabel("Height (m):")
        layout.addWidget(self.height_label)
        self.height_entry = QLineEdit()
        layout.addWidget(self.height_entry)

        self.calculate_button = QPushButton("Calculate BMI")
        self.calculate_button.clicked.connect(self.calculate_bmi)
        layout.addWidget(self.calculate_button)

        self.bmi_result = QLabel("")
        layout.addWidget(self.bmi_result)

        self.view_history_button = QPushButton("View History")
        self.view_history_button.clicked.connect(self.view_history)
        layout.addWidget(self.view_history_button)

        self.plot_trend_button = QPushButton("Plot Trend")
        self.plot_trend_button.clicked.connect(self.plot_trend)
        layout.addWidget(self.plot_trend_button)

        self.setLayout(layout)
    def view_history(self):
        c.execute("SELECT * FROM bmi_entries")
        entries = c.fetchall()

        table = QTableWidget()
        table.setColumnCount(5)  
        table.setHorizontalHeaderLabels([ "Weight", "Height", "BMI", "Date"])
        screen = QApplication.primaryScreen()
        size = screen.size()
        width = size.width() * 0.7
        height = size.height() * 0.4
        table.setFixedSize(int(width), int(height))

        for row_number, entry in enumerate(entries):
            table.insertRow(row_number)
            for column_number, data in enumerate(entry):
                table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        msg = QMessageBox()
        msg.setWindowTitle("BMI History")
        msg.setIcon(QMessageBox.Information)
        msg.setText("History:")
        msg.layout().addWidget(table)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def calculate_bmi(self):
        weight = float(self.weight_entry.text())
        height = float(self.height_entry.text())
        bmi = weight / (height ** 2)
        self.bmi_result.setText("BMI: {:.2f}".format(bmi))
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO bmi_entries (weight, height, bmi, date) VALUES (?, ?, ?, ?)", (weight, height, bmi, date))
        connect.commit()

    def plot_trend(self):
        c.execute("SELECT date, bmi FROM bmi_entries")
        entries = c.fetchall()
        dates = [entry[0] for entry in entries]
        bmis = [entry[1] for entry in entries]
        plt.plot(dates, bmis)
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.title("BMI Trend Over Time")
        plt.xticks(rotation=45)
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BMI()
    window.show()
    sys.exit(app.exec_())
