
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QTabWidget, QTableWidget, \
    QTableWidgetItem, QLabel, QPushButton, QLineEdit, QMessageBox, QComboBox, QCalendarWidget


    class ElectronicJournalApp(QMainWindow):
    def init(self):
        super().init()

        self.setWindowTitle("Журнал Пропусков")
        self.setGeometry(100, 100, 800, 600)

        self.students_data = {}  # Словарь для хранения данных о студентах
        self.load_students_data()  # Загружаем данные при запуске

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        
        self.setWindowOpacity(0.91)
        
        
        self.group_combo = QComboBox()
        self.group_combo.addItem("ИСТ-311")
        self.group_combo.addItem("ПИ-311")

        self.subject_combo = QComboBox()
        self.subject_combo.addItem("Математика")
        self.subject_combo.addItem("Физика")
        self.subject_combo.addItem("История России")

        self.calendar = QCalendarWidget(self)

        self.attendance_table = QTableWidget()
        self.attendance_table.setRowCount(10)
        self.attendance_table.setColumnCount(4)
        self.attendance_table.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Пропуск"])

        view_group_button = QPushButton("Просмотр группы")
        view_group_button.clicked.connect(self.view_group)
        view_attendance_button = QPushButton("Просмотр посещаемости")
        view_attendance_button.clicked.connect(self.view_attendance)

        mark_attendance_button = QPushButton("Отметить посещаемость")
        save_date = QPushButton('Сохранить')
        save_date.clicked.connect(self.save_data)

        main_layout.addWidget(self.group_combo)
        main_layout.addWidget(self.subject_combo)
        main_layout.addWidget(self.calendar)
        main_layout.addWidget(view_group_button)  
        main_layout.addWidget(self.attendance_table)
        main_layout.addWidget(mark_attendance_button)
        main_layout.addWidget(view_attendance_button)  
        main_layout.addWidget(save_date)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def view_attendance(self):
        """Отображает данные о посещаемости из файла attendance.txt."""
        group = self.group_combo.currentText()
        subject = self.subject_combo.currentText()

        try:
            with open("attendance.txt", "r", encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", "Файл attendance.txt не найден!")
            return

        self.attendance_table.clearContents() 
        row_index = 0
        for line in lines:
            if line.startswith(f"Группа: {group} Предмет: {subject}"):
                for line in lines[row_index + 3:]:  
                    if not line.strip():  
                        break
                    last_name, first_name, patronymic, attendance = line.strip().split("\t")
                    self.attendance_table.insertRow(row_index)  
                    self.attendance_table.setItem(row_index, 0, QTableWidgetItem(last_name))
                    self.attendance_table.setItem(row_index, 1, QTableWidgetItem(first_name))
                    self.attendance_table.setItem(row_index, 2, QTableWidgetItem(patronymic))
                    self.attendance_table.setItem(row_index, 3, QTableWidgetItem(attendance))
                    row_index += 1
                break  
            row_index += 1
    def load_students_data(self):
        
        try:
            with open("students.txt", "r", encoding='utf-8') as f:
                for line in f:
                    group, last_name, first_name, patronymic = line.strip().split(",")
                    if group not in self.students_data:
                        self.students_data[group] = []
                    self.students_data[group].append((last_name, first_name, patronymic))
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", "Файл students.txt не найден!")

    def view_group(self):
        
        group = self.group_combo.currentText()
        self.attendance_table.clearContents()  # Очищаем таблицу
        if group in self.students_data:
            students = self.students_data[group]
            self.attendance_table.setRowCount(len(students))
            for row, student in enumerate(students):
                for col, data in enumerate(student):
                    item = QTableWidgetItem(data)
                    self.attendance_table.setItem(row, col, item)

    def save_data(self):
        group = self.group_combo.currentText()
        subject = self.subject_combo.currentText()
        date = self.calendar.selectedDate().toString("dd MMMM")  
        data = [f"Группа: {group}\n", f"Предмет: {subject}\n", f"Дата: {date}\n\n"]

        flag = False

        for row in range(self.attendance_table.rowCount()):
            row_data = []
            for col in range(self.attendance_table.columnCount()):
                item = self.attendance_table.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    flag = True
                    break
            if flag:
                break
            data.append(
                f"{row_data[0]}\t{row_data[1]}\t{row_data[2]}\t{'Отсутствует(У)' if row_data[3] == '1' else 'Отсутствует(Н)'}\n")

        try:
            with open("attendance.txt", "a", encoding='utf-8') as f:
                f.writelines(data)
            QMessageBox.information(self, "Успех", "Данные сохранены в файл attendance.txt")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить данные: {str(e)}")


    if __name__ == '__main__':
    app = QApplication(sys.argv)

    journal_app = ElectronicJournalApp()
    journal_app.show()
    sys.exit(app.exec_())
