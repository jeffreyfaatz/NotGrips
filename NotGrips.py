import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem

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
        layout = QVBoxLayout()

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        layout.addWidget(self.first_name_input)

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        layout.addWidget(self.last_name_input)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("9-digit ID Number")
        layout.addWidget(self.id_input)

        self.Bin_input = QLineEdit()
        self.Bin_input.setPlaceholderText("Number (1-670)")
        layout.addWidget(self.Bin_input)

        self.Unit = QComboBox()
        self.Unit.addItems(["A1", "A2", "B1", "B2", "B3", "C1", "C2", "C3", "C4", "SHU", "MHU"])
        layout.addWidget(self.Unit)

        self.Bed_input = QLineEdit()
        self.Bed_input.setPlaceholderText("3-digit Subgroup")
        layout.addWidget(self.Bed_input)

        self.date_input = QDateEdit()
        layout.addWidget(self.date_input)

        self.level_combo = QComboBox()
        self.level_combo.addItems(["L", "ML", "MH", "MHV", "H"])
        layout.addWidget(self.level_combo)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_person)
        layout.addWidget(self.save_button)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Criteria")
        layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_person)
        layout.addWidget(self.search_button)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(["First Name", "Last Name", "ID", "Bin", "Unit", "Bed", "Date", "Level"])
        layout.addWidget(self.table_widget)

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
        Bin = self.number_input.text()  # Update this line
        Unit = self.group_combo.currentText()
        Bed = self.subgroup_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")
        level = self.level_combo.currentText()

        # Validate the input data as needed

        self.cursor.execute("""
            INSERT INTO persons (first_name, last_name, id_number, Bin, Unit, Bed, date, level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, id_number, Bin, Unit, Bed, date, level))
        self.conn.commit()

        print("Data saved to the database.")



    def search_person(self):
        search_text = self.search_input.text()

        self.cursor.execute("""
            SELECT * FROM persons
            WHERE first_name LIKE ? OR last_name LIKE ? OR id_number LIKE ? OR Bin LIKE ?  -- Update this line
        """, ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))

        results = self.cursor.fetchall()
        self.populate_table(results)



    def populate_table(self, data):
        self.table_widget.setRowCount(0)

        for row_num, row_data in enumerate(data):
            self.table_widget.insertRow(row_num)
            for col_num, cell_data in enumerate(row_data):
                self.table_widget.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))




def main():
    app = QApplication(sys.argv)
    window = PersonDatabaseApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()