def load_students_data(self):
        """Загружает данные о студентах из файла students.txt."""
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
        """Отображает студентов выбранной группы в таблице."""
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
        date = self.calendar.selectedDate().toString("dd MMMM")  # Получаем дату из календаря
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


if name == 'main':
    app = QApplication(sys.argv)

    journal_app = ElectronicJournalApp()
    journal_app.show()
    sys.exit(app.exec_())
