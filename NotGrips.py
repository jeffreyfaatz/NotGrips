import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QHBoxLayout
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QDate


class PersonDatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NotGrips Jail Management")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.init_ui()
        self.init_database()

    def init_ui(self):
        layout = QHBoxLayout()  # Use a horizontal layout to split the window

        # Left column for input fields and buttons
        left_layout = QVBoxLayout()

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        self.first_name_input.setMinimumHeight(30)  # Increase the height by setting the minimum height
        left_layout.addWidget(self.first_name_input)

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.last_name_input.setMinimumHeight(30)
        left_layout.addWidget(self.last_name_input)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("9-digit ID Number")
        self.id_input.setMinimumHeight(30)
        left_layout.addWidget(self.id_input)

        self.Bin_input = QLineEdit()
        self.Bin_input.setPlaceholderText("Number (1-670)")
        self.Bin_input.setMinimumHeight(30)

        # Add QIntValidator to enforce integer input within the specified range
        validator = QIntValidator(1, 670)
        self.Bin_input.setValidator(validator)

        left_layout.addWidget(self.Bin_input)


        self.Unit = QComboBox()
        self.Unit.addItems(["A1", "A2", "B1", "B2", "B3", "C1", "C2", "C3", "C4", "SHU", "MHU"])
        self.Unit.setMinimumHeight(30)
        left_layout.addWidget(self.Unit)

        self.Bed_input = QLineEdit()
        self.Bed_input.setPlaceholderText("3-digit Subgroup")
        self.Bed_input.setMinimumHeight(30)
        left_layout.addWidget(self.Bed_input)

        self.level_combo = QComboBox()
        self.level_combo.addItems(["L", "ML", "MH", "MHV", "H"])
        self.level_combo.setMinimumHeight(30)
        left_layout.addWidget(self.level_combo)

        self.date_input = QDateEdit(QDate.currentDate())  # Set the current date
        self.date_input.setMinimumHeight(30)
        left_layout.addWidget(self.date_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_person)
        left_layout.addWidget(self.save_button)

        # Right column for the table widget
        right_layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(["First Name", "Last Name", "ID", "Bin", "Unit", "Bed", "Date", "Level"])
        right_layout.addWidget(self.table_widget)

        # Add both left and right layouts to the main layout
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        # Create a sub-layout for search and report buttons
        sub_layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Criteria")
        self.search_input.setMinimumHeight(30)
        sub_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_person)
        self.search_button.setMinimumHeight(30)
        sub_layout.addWidget(self.search_button)

        self.run_report_button = QPushButton("Run Report")
        self.run_report_button.clicked.connect(self.show_all_records)
        self.run_report_button.setMinimumHeight(30)
        sub_layout.addWidget(self.run_report_button)

        # Add the sub-layout to the left column
        left_layout.addLayout(sub_layout)

        self.central_widget.setLayout(layout)


    def init_database(self):
        self.conn = sqlite3.connect("person_database.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                id_number TEXT,
                Bin INTEGER,
                Unit TEXT,
                Bed TEXT,
                date TEXT,
                level TEXT
            )
        """)
        self.conn.commit()

    def save_person(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        id_number = self.id_input.text()
        Bin = self.Bin_input.text()
        Unit = self.Unit.currentText()
        Bed = self.Bed_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")
        level = self.level_combo.currentText()

        # Check if the ID number is 9 digits
        if len(id_number) != 9:
            QMessageBox.warning(self, "Invalid ID Number", "Alien number must be 9 digits")
            return  # Exit the method without saving

        # Validate the input data as needed

        self.cursor.execute("""
            INSERT INTO persons (first_name, last_name, id_number, Bin, Unit, Bed, date, level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, id_number, Bin, Unit, Bed, date, level))
        self.conn.commit()

        print("Data saved to the database.")



    def search_person(self):
        search_text = self.search_input.text()

        # Specify the columns you want to retrieve, excluding the "ID" column
        self.cursor.execute("""
            SELECT first_name, last_name, id_number, Bin, Unit, Bed, date, level
            FROM persons
            WHERE first_name LIKE ? OR last_name LIKE ? OR id_number LIKE ? OR Bin LIKE ?
        """, ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))

        results = self.cursor.fetchall()

        if not results:
            QMessageBox.information(self, "No Results", "No results to match your search.")
        else:
            self.populate_table(results)


    def populate_table(self, data):
        self.table_widget.setRowCount(0)

        for row_num, row_data in enumerate(data):
            self.table_widget.insertRow(row_num)
            for col_num, cell_data in enumerate(row_data):
                self.table_widget.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))

    def show_all_records(self):
        self.cursor.execute("SELECT * FROM persons")
        results = self.cursor.fetchall()
        
        if not results:
            QMessageBox.information(self, "No Records", "There are no records in the database.")
        else:
            self.populate_table(results)

    def sort_table(self, logical_index):
        self.table_widget.sortItems(logical_index)



def main():
    app = QApplication(sys.argv)
    window = PersonDatabaseApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
