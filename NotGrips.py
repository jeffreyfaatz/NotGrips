import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QHBoxLayout
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QDate, Qt


class PersonDatabaseApp(QMainWindow):
    
    # Define the unit_bed_options dictionary here as a class attribute
    unit_bed_options = {
        "A1": ["110A", "110B", "111A", "111B", "112A", "112B", "113A", "113B", "114A", "114B", "115A", "115B", "116A", "116B", "117A", "117B", "118A", "118B", "119A", "119B", "120A", "120B"],
        "A2": ["121A", "121B", "122A", "122B", "123A", "123B", "124A", "124B", "125A", "125B", "126A", "126B", "127A", "127B", "128A", "128B", "129A", "129B", "130A", "130B"],
        "B1": ["131A", "131B", "132A", "132B", "133A", "133B", "134A", "134B", "135A", "135B", "136A", "136B", "137A", "137B", "138A", "138B", "139A", "139B", "140A", "140B"],
        "B2": [str(i) for i in range(141, 201)],
        "B3": [str(i) for i in range(201, 262)],
        "C1": [str(i) for i in range(262, 321)],
        "C2": [str(i) for i in range(321, 382)],
        "C3": [str(i) for i in range(382, 441)],
        "C4": [str(i) for i in range(441, 501)],
        "SHU": [str(i) for i in range(110, 145)],
        "MHU": ["118A", "118B", "122", "123"]
    }
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NotGrips Jail Management")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.init_ui()
        self.init_database()
        self.load_used_options()  # Load used options on application startup

        self.update_bed_options()  #Update Bed options on startup

    def init_ui(self):
        layout = QHBoxLayout()  # Use a horizontal layout to split the window

        # Left column for input fields and buttons
        left_layout = QVBoxLayout()

        first_name_label = QLabel("First Name:")
        left_layout.addWidget(first_name_label)

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        self.first_name_input.setMinimumHeight(30)  # Increase the height by setting the minimum height
        left_layout.addWidget(self.first_name_input)

        last_name_label = QLabel("Last Name:")
        left_layout.addWidget(last_name_label)

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.last_name_input.setMinimumHeight(30)
        left_layout.addWidget(self.last_name_input)

        id_label = QLabel("Alien Number:")
        left_layout.addWidget(id_label)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Alien Number")
        self.id_input.setMinimumHeight(30)
        left_layout.addWidget(self.id_input)

        Bin_label = QLabel("Bin:")
        left_layout.addWidget(Bin_label)

        self.Bin_input = QComboBox()

        for i in range(1, 671):
            self.Bin_input.addItem(str(i))

        self.Bin_input.setCurrentIndex(-1)
        self.Bin_input.setMinimumHeight(30)
        left_layout.addWidget(self.Bin_input)

        Unit_label = QLabel("Unit:")
        left_layout.addWidget(Unit_label)

        self.Unit = QComboBox()
        self.Unit.addItems(["A1", "A2", "B1", "B2", "B3", "C1", "C2", "C3", "C4", "SHU", "MHU"])
        self.Unit.setMinimumHeight(30)
        self.Unit.setCurrentIndex(-1)  # Set to no current index
        left_layout.addWidget(self.Unit)

        Bed_label = QLabel("Bed:")
        left_layout.addWidget(Bed_label)

        self.Bed_input = QComboBox()  # Change to QComboBox
        self.Bed_input.setPlaceholderText("Bed")
        self.Bed_input.setMinimumHeight(30)
        self.Bed_input.setCurrentIndex(-1)  # Set to no current index
        left_layout.addWidget(self.Bed_input)

        level_label = QLabel("Level:")
        left_layout.addWidget(level_label)

        self.level_combo = QComboBox()
        self.level_combo.addItems(["L", "ML", "MH", "MHV", "H"])
        self.level_combo.setMinimumHeight(30)
        self.level_combo.setCurrentIndex(-1)  # Set to no current index
        left_layout.addWidget(self.level_combo)

        self.date_input = QDateEdit(QDate.currentDate())  # Set the current date
        self.date_input.setMinimumHeight(30)
        left_layout.addWidget(self.date_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_person)
        left_layout.addWidget(self.save_button)

        # Connect the Unit combo box to the update_bed_options method
        self.Unit.currentTextChanged.connect(self.update_bed_options)

        # Right column for the table widget
        right_layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(["First Name", "Last Name", "ID", "Bin", "Unit", "Bed", "Date", "Level"])
        right_layout.addWidget(self.table_widget)

        # Enable sorting for the QTableWidget:
        self.table_widget.setSortingEnabled(True)

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

        # Add the "Release" button for deleting rows
        self.release_button = QPushButton("Release")
        self.release_button.clicked.connect(self.release_person)
        sub_layout.addWidget(self.release_button)

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

    def update_bed_options(self):
        selected_unit = self.Unit.currentText()
        bed_options = self.unit_bed_options.get(selected_unit, [])
        self.Bed_input.clear()
        self.Bed_input.addItems(bed_options)

    def save_person(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        id_number = self.id_input.text()
        Bin = self.Bin_input.currentText()
        Unit = self.Unit.currentText()
        Bed = self.Bed_input.currentText()
        date = self.date_input.date().toString("yyyy-MM-dd")
        level = self.level_combo.currentText()

        # Check if the ID number is 9 digits
        if len(id_number) != 9:
            QMessageBox.warning(self, "Invalid ID Number", "Alien number must be 9 digits")
            return  # Exit the method without saving

        # Check if the ID number is already in use
        if self.is_id_number_used(id_number):
            QMessageBox.warning(self, "Duplicate Alien Number", "Alien number is already in use. Please enter a new 9-digit number.")
            self.id_input.clear()  # Clear the input to allow entering a new number
            return  # Exit the method without saving

        try:
            with self.conn:
                self.cursor.execute("""
                    INSERT INTO persons (first_name, last_name, id_number, Bin, Unit, Bed, date, level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (first_name, last_name, id_number, Bin, Unit, Bed, date, level))
            # Remove the used options from drop-downs
            self.remove_used_options(Bin, Unit, Bed)
            print("Data saved to the database.")
        except sqlite3.Error as e:
            print("Error:", e)


    def is_id_number_used(self, id_number):
        self.cursor.execute("SELECT id_number FROM persons WHERE id_number = ?", (id_number,))
        result = self.cursor.fetchone()
        return result is not None

    def remove_used_options(self, Bin, Unit, Bed):
        # Remove used options from the respective drop-downs
        if Unit in self.unit_bed_options:
            self.unit_bed_options[Unit].remove(Bed)
        self.Bin_input.removeItem(self.Bin_input.findText(Bin))
        self.Bed_input.removeItem(self.Bed_input.findText(Bed))

    def release_person(self):
        # Get the selected row
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            # Fetch the ID number from the database using the row index
            id_number = self.table_widget.item(selected_row, 2).text()
            self.cursor.execute("DELETE FROM persons WHERE id_number = ?", (id_number,))
            self.conn.commit()
            # Remove the row from the table
            self.table_widget.removeRow(selected_row)


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
        self.cursor.execute("""
            SELECT first_name, last_name, id_number, Bin, Unit, Bed, date, level
            FROM persons
        """)
        results = self.cursor.fetchall()

        if not results:
            QMessageBox.information(self, "No Records", "There are no records in the database.")
        else:
            self.populate_table(results)


    def sort_table(self, logical_index):
        self.table_widget.sortItems(logical_index)

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

    def load_used_options(self):
        # Load used options (Bin, Unit, Bed) from the database
        self.cursor.execute("SELECT Bin, Unit, Bed FROM persons")
        used_options = self.cursor.fetchall()

        for option in used_options:
            Bin, Unit, Bed = option
            # Disable the used options in their respective drop-downs
            if Bin:
                self.Bin_input.removeItem(self.Bin_input.findText(str(Bin)))  # Convert Bin to a string before adding it
            if Unit:
                self.Unit.addItem(Unit)
            if Bed:
                self.Bed_input.addItem(Bed)


def main():
    app = QApplication(sys.argv)
    window = PersonDatabaseApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
