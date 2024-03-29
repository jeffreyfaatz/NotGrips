import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QHBoxLayout
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QDate, Qt

class PersonDatabaseApp(QMainWindow):
    
    # Define the unit_bed_options dictionary here as a class attribute
    unit_bed_options = {
        "A1 LOWER": ["104A", "104B", "106A", "106B", "107A", "107B", "109A", "109B", "110A", "110B", "112A", "112B", "113A", "113B", "115A", "115B", "116A", "116B", "118A", "118B", "119A-H", "121A", "121B", "122A", "122B", "124A", "124B", "125A", "125B", "127A", "127B", "128A", "128B", "130A", "130B", "131-SHU", "133-SHU", "134-SHU", "136A-H", "137-SHU"],
        "A1 UPPER": ["201A", "201B", "203A", "203B", "204A", "204B", "206A", "206B", "207A", "207B", "209A", "209B", "210A", "210B", "212A", "212B", "213A", "213B", "215A", "215B", "216A", "216B", "218A", "218B", "219A", "219B", "221A", "221B", "222A", "222B", "224A", "224B", "225A", "225B", "227A", "227B", "228A", "228B", "230A", "230B", "231A", "231B", "233A", "233B", "234A", "234B", "236A", "236B"],
        "A2 LOWER": ["143A", "143B", "144A", "144B", "146A", "146B", "147A", "147B", "149A", "149B", "150A", "150B", "152A", "152B", "153A", "153B", "155A", "155B", "156A", "156B", "158A", "158B", "159A-H", "161A", "161B", "162A", "162B", "164A", "164B", "165A", "165B", "167A", "167B", "168A", "168B", "170A", "170B", "171A", "171B", "173A", "173B", "174A", "174B", "176A-H", "177A", "177B"],
        "A2 UPPER": ["241A", "241B", "243A", "243B", "244A", "244B", "246A", "246B", "247A", "247B", "249A", "249B", "250A", "250B", "252A", "252B", "253A", "253B", "255A", "255B", "256A", "256B", "258A", "258B", "259A", "259B", "261A", "261B", "262A", "262B", "264A", "264B", "265A", "265B", "267A", "267B", "268A", "268B", "270A", "270B", "271A", "271B", "273A", "273B", "274A", "274B", "276A", "276B"],
        "B1 LOWER": ["103A", "103B", "104A", "104B", "106A", "106B", "107A", "107B", "109A", "109B", "110A", "110B", "112A", "112B", "113A", "113B", "115A", "115B", "116A", "116B", "118A", "118B", "119A-H", "121A", "121B", "122A", "122B", "124A", "124B", "125A", "125B", "127A", "127B", "128A", "128B", "130A", "130B", "131A", "131B", "133A", "133B", "134A", "134B", "136A-H", "137A", "137B"],
        "B1 UPPER": ["201A", "201B", "203A", "203B", "204A", "204B", "206A", "206B", "207A", "207B", "209A", "209B", "210A", "210B", "212A", "212B", "213A", "213B", "215A", "215B", "216A", "216B", "218A", "218B", "219A", "219B", "221A", "221B", "222A", "222B", "224A", "224B", "225A", "225B", "227A", "227B", "228A", "228B", "230A", "230B", "231A", "231B", "233A", "233B", "234A", "234B", "236A", "236B"],
        "B2": [(str(i) for i in range(1, 60)), "361", "362", "363", "364"],
        "B3": [(str(i) for i in range(61, 120)), "365", "366", "367", "368"],
        "C1": [(str(i) for i in range(121, 180)), "369", "370", "371", "372"],
        "C2": [(str(i) for i in range(181, 240)), "373", "374", "375", "376"],
        "C3": [(str(i) for i in range(241, 300)), "377", "378", "379", "390"],
        "C4": [(str(i) for i in range(301, 360)), "381", "382", "383", "384"],
        "SHU": [],
        "MHU": ["118A", "118B", "122", "123"],
    }
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NotGrips Jail Management")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.init_ui()
        self.init_database()
        self.update_bed_options()  #Update Bed options on startup
        self.load_used_options()  # Load used options on application startup

        

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

        birth_date_label = QLabel("DOB")
        left_layout.addWidget(birth_date_label)

        self.birth_date_input = QLineEdit()
        self.birth_date_input.setPlaceholderText("DOB")
        self.birth_date_input.setMinimumHeight(30)
        left_layout.addWidget(self.birth_date_input)

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

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_person)
        left_layout.addWidget(self.edit_button)

        # Connect the Unit combo box to the update_bed_options method
        self.Unit.currentTextChanged.connect(self.update_bed_options)

        # Right column for the table widget
        right_layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(9)
        self.table_widget.setHorizontalHeaderLabels(["First Name", "Last Name", "ID", "DOB", "Bin", "Unit", "Bed", "Date", "Level"])
        right_layout.addWidget(self.table_widget)

        # Enable sorting for the QTableWidget:
        self.table_widget.setSortingEnabled(True)

        # Add both left and right layouts to the main layout
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        # Create a sub-layout for buttons
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
        self.release_button.setMinimumHeight(30)
        sub_layout.addWidget(self.release_button)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_database)
        self.refresh_button.setMinimumHeight(30)
        sub_layout.addWidget(self.refresh_button)


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
                id_number INTEGER,
                birth_date DATE,
                Bin INTEGER,
                Unit TEXT,
                Bed TEXT,
                date DATE,
                level TEXT
            )
        """)
        self.conn.commit()

    def update_bed_options(self):
        selected_unit = self.Unit.currentText()
        bed_options = self.unit_bed_options.get(selected_unit, [])
        self.Bed_input.clear()
        self.Bed_input.addItems(bed_options)

    def load_used_options(self):
        # Load used options (Bin, Unit, Bed) from the database
        self.cursor.execute("SELECT DISTINCT Bin, Unit, Bed FROM persons")
        used_options = self.cursor.fetchall()

        for option in used_options:
            Bin, Unit, Bed = option
            # Disable the used options in their respective drop-downs
            if Bin:
                self.Bin_input.removeItem(self.Bin_input.findText(str(Bin)))  # Convert Bin to a string before adding it
            if Bed:
                self.Bed_input.removeItem(self.Bed_input.findText(Bed))
                if Unit in self.unit_bed_options and Bed in self.unit_bed_options[Unit]:
                    self.unit_bed_options[Unit].remove(Bed)

    def save_person(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        id_number = self.id_input.text()
        birth_date = self.birth_date_input.text()
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
            # If the ID number is in use, check if it's the same as the original ID
            # number of the record being edited
            selected_row = self.table_widget.currentRow()
            if selected_row >= 0:
                original_id_number_item = self.table_widget.item(selected_row, 2)
                if original_id_number_item is not None:
                    original_id_number = original_id_number_item.text()
                    if id_number == original_id_number:
                        # The edited ID number is the same as the original, no need to check for duplicates
                        pass
                    else:
                        QMessageBox.warning(self, "Duplicate Alien Number", "Alien number is already in use. Please enter a new 9-digit number.")
                        self.id_input.clear()  # Clear the input to allow entering a new number
                        return  # Exit the method without saving

        try:
            with self.conn:
                # If you're editing an existing record, use an UPDATE statement instead of INSERT
                selected_row = self.table_widget.currentRow()
                if selected_row >= 0:
                    original_id_number_item = self.table_widget.item(selected_row, 2)
                    if original_id_number_item is not None:
                        original_id_number = original_id_number_item.text()
                        self.update_person(original_id_number, first_name, last_name, id_number, birth_date, Bin, Unit, Bed, date, level)
                else:
                    # This is a new record, insert it into the database
                    self.insert_person(first_name, last_name, id_number, birth_date, Bin, Unit, Bed, date, level)

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
        if Unit in self.unit_bed_options and Bed in self.unit_bed_options[Unit]:
            self.unit_bed_options[Unit].remove(Bed)  # Check if Bed exists in the list before removing
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
            SELECT first_name, last_name, id_number, birth_date, Bin, Unit, Bed, date, level
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
            SELECT first_name, last_name, id_number, birth_date, Bin, Unit, Bed, date, level
            FROM persons
        """)
        results = self.cursor.fetchall()

        if not results:
            QMessageBox.information(self, "No Records", "There are no records in the database.")
        else:
            self.populate_table(results)


    def sort_table(self, logical_index):
        self.table_widget.sortItems(logical_index)

    def refresh_database(self):
        # Clear existing data in the table widget
        self.table_widget.setRowCount(0)

        # Reload the data from the database for beds and bins
        self.load_used_options()

        # Update the Bed and Bin options
        self.update_bed_options()
        self.update_bin_options()

        # Show all records in the table widget
        self.show_all_records()

    def update_bin_options(self):
        used_bins = self.get_used_bins()
        all_bins = [str(i) for i in range(1, 671)]

        # Remove used bins from all_bins
        available_bins = [bin for bin in all_bins if bin not in used_bins]

        self.Bin_input.clear()
        self.Bin_input.addItems(available_bins)

    def get_used_bins(self):
        self.cursor.execute("SELECT DISTINCT Bin FROM persons WHERE Bin IS NOT NULL")
        used_bins = [str(row[0]) for row in self.cursor.fetchall()]
        return used_bins
    
    def edit_person(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            # Get the data from the selected row if it exists
            for col_num in range(self.table_widget.columnCount()):
                item = self.table_widget.item(selected_row, col_num)
                if item is not None:
                    text = item.text()
                    # Set the corresponding input field with the data from the selected row
                    if col_num == 0:
                        self.first_name_input.setText(text)
                    elif col_num == 1:
                        self.last_name_input.setText(text)
                    elif col_num == 2:
                        self.id_input.setText(text)
                    elif col_num == 3:
                        self.birth_date_input.setText(text)
                    elif col_num == 4:
                        self.Bin_input.setCurrentText(str(text))  # Use setCurrentText for QComboBox
                    elif col_num == 5:
                        self.Unit.setCurrentText(text)
                    elif col_num == 6:
                        self.Bed_input.setCurrentText(text)  # Use setCurrentText for QComboBox
                    elif col_num == 7:
                        self.date_input.setDate(QDate.fromString(text, "yyyy-MM-dd"))
                    elif col_num == 8:
                        self.level_combo.setCurrentText(text)






    def insert_person(self, first_name, last_name, id_number, birth_date, Bin, Unit, Bed, date, level):
        try:
            with self.conn:
                self.cursor.execute("""
                    INSERT INTO persons (first_name, last_name, id_number, birth_date, Bin, Unit, Bed, date, level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (first_name, last_name, id_number, birth_date, Bin, Unit, Bed, date, level))

        except sqlite3.Error as e:
            print("Error:", e)

    def update_person(self, id_number, first_name, last_name, new_id_number, birth_date, Bin, Unit, Bed, date, level):
        try:
            with self.conn:
                self.cursor.execute("""
                    UPDATE persons
                    SET first_name = ?, last_name = ?, id_number = ?, birth_date = ?, Bin = ?, Unit = ?, Bed = ?, date = ?, level = ?
                    WHERE id_number = ?
                """, (first_name, last_name, new_id_number, birth_date, Bin, Unit, Bed, date, level, id_number))

        except sqlite3.Error as e:
            print("Error:", e)


def main():
    app = QApplication(sys.argv)
    window = PersonDatabaseApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
