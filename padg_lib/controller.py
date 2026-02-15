from tkinter import *
from padg_lib.view import MapView
from padg_lib.model import University, Class, Employee, Student, universities, classes, employees, students, get_coordinates


class MapController:
    def __init__(self, root: Tk, view: MapView):
        self.root = root
        self.view = view

        self.view.combobox_kategoria.bind("<<ComboboxSelected>>", self.category_selection)

        self.universities_data:list = universities
        self.displayed_universities:list = list(universities)
        self.employees_data:list = employees
        self.displayed_employees:list = list(employees)
        self.students_data:list = students
        self.displayed_students:list = list(students)
        self.classes_data:list = classes

        self.markers: dict = {}

        self.view.button_add_university.config(command=lambda: self.add_university())
        self.view.button_delete_university.config(command=lambda: self.delete_university())
        self.view.button_edit_university.config(command=lambda: self.edit_university())
        self.view.button_show_on_map.config(command=self.show_universities_on_map)
        self.view.button_reset_university_filter.config(command=self.reset_university_filters)

        self.view.button_add_employee.config(command=lambda: self.add_employee())
        self.view.button_delete_employee.config(command=lambda: self.delete_employee())
        self.view.button_edit_employee.config(command=lambda: self.edit_employee())
        self.view.button_filter_employees.config(command=self.filter_employees)
        self.view.button_reset_employee_filter.config(command=self.reset_employee_filters)

        self.view.button_add_class.config(command=lambda: self.add_class())
        self.view.button_delete_class.config(command=lambda: self.delete_class())
        self.view.button_edit_class.config(command=lambda: self.edit_class())

        self.view.button_add_student.config(command=lambda: self.add_student())
        self.view.button_delete_student.config(command=lambda: self.delete_student())
        self.view.button_edit_student.config(command=lambda: self.edit_student())
        self.view.button_filter_students.config(command=self.filter_students)
        self.view.button_reset_student_filter.config(command=self.reset_student_filters)

        self.view.combobox_university_for_student.bind("<<ComboboxSelected>>", self.update_class_combobox)
        self.view.entry_student_filter_university.bind("<<ComboboxSelected>>", self.update_student_filter_class_combobox)

        self.university_info()
        self.employee_info()
        self.class_info()
        self.student_info()


    def category_selection(self, event):
        selected_category = self.view.selected_category.get()
        self.view.show_frame(selected_category)
        if selected_category == "Uczelnie":
            self.show_universities_on_map()
        elif selected_category == "Pracownicy":
            self.filter_employees()
        elif selected_category == "Studenci":
            self.filter_students()
        else:
            for obj, marker_instance in self.markers.items():
                marker_instance.delete()
            self.markers = {}


    def show_universities_on_map(self):
        city_filter = self.view.entry_map_city_filter.get()

        self.view.listbox_universities.delete(0, END)

        if city_filter:
            self.displayed_universities = [university for university in self.universities_data if university.city.lower() == city_filter.lower()]
        else:
            self.displayed_universities = list(self.universities_data)

        if self.view.selected_category.get() == "Uczelnie":
            for obj, marker_instance in self.markers.items():
                marker_instance.delete()
            self.markers = {}
            
            for idx, university in enumerate(self.displayed_universities):
                if hasattr(university, 'coords') and university.coords:
                    marker = self.view.map_widget.set_marker(university.coords[0], university.coords[1], text=university.name)
                    self.markers[university] = marker
                self.view.listbox_universities.insert(idx, f"{university.name} {university.city} {university.street}")
        else:
            for idx, university in enumerate(self.displayed_universities):
                self.view.listbox_universities.insert(idx, f"{university.name} {university.city} {university.street}")



    def reset_university_filters(self):
        self.view.entry_map_city_filter.delete(0, END)
        self.show_universities_on_map()

    def reset_employee_filters(self):
        self.view.entry_employee_filter_city.delete(0, END)
        self.view.entry_employee_filter_university.set('')
        self.filter_employees()

    def reset_student_filters(self):
        self.view.entry_student_filter_university.set('')
        self.view.entry_student_filter_class.set('')
        self.filter_students()


############Uczelnie############

    def university_info(self):
        self.show_universities_on_map()

        university_names = [university.name for university in self.universities_data]
        self.view.entry_employee_university['values'] = university_names
        self.view.entry_employee_filter_university['values'] = university_names

    def add_university(self) -> None:
        name: str = self.view.entry_university_name.get()
        city: str = self.view.entry_university_city.get()
        street: str = self.view.entry_university_street.get()
        university = University(name=name, city=city, street=street)
        self.universities_data.append(university)
        self.university_info()
        self.class_info()
        self.view.entry_university_name.delete(0, END)
        self.view.entry_university_city.delete(0, END)
        self.view.entry_university_street.delete(0, END)
        self.student_info()

    def delete_university(self):
        i = self.view.listbox_universities.index(ACTIVE)
        university_to_delete = self.displayed_universities[i]

        university_name_to_delete = university_to_delete.name

        if university_to_delete in self.markers:
            self.markers[university_to_delete].delete()
        
        if university_to_delete in self.universities_data:
            self.universities_data.remove(university_to_delete)
        
        self.university_info()

        employees_to_keep = []
        for employee in self.employees_data:
            if employee.university_name != university_name_to_delete:
                employees_to_keep.append(employee)
            else:
                if employee in self.markers:
                    self.markers[employee].delete()

        self.employees_data = employees_to_keep

        classes_to_keep = []
        for class_ in self.classes_data:
            if class_.university_name != university_name_to_delete:
                classes_to_keep.append(class_)

        self.classes_data = classes_to_keep
        self.class_info()
        self.employee_info()
        self.class_info()
        self.student_info()

    def edit_university(self):
            if not self.universities_data:
                return

            i = self.view.listbox_universities.index(ACTIVE)
            university = self.displayed_universities[i]

            self.view.entry_university_name.delete(0, END)
            self.view.entry_university_city.delete(0, END)
            self.view.entry_university_street.delete(0, END)
            self.view.entry_university_name.insert(0, university.name)
            self.view.entry_university_city.insert(0, university.city)
            self.view.entry_university_street.insert(0, university.street)
            self.view.button_add_university.config(
                text="Zapisz zmiany",
                command=lambda: self.update_university(university)
            )
   
    def update_university(self, university):
        old_university_name = university.name

        university.name = self.view.entry_university_name.get()
        university.city = self.view.entry_university_city.get()
        university.street = self.view.entry_university_street.get()
        address = f"{university.city}, {university.street}"
        university.coords = get_coordinates(address)

        if university in self.markers:
            marker = self.markers[university]
            marker.set_position(university.coords[0], university.coords[1])
            marker.set_text(university.name)

        for employee in self.employees_data:
            if employee.university_name == old_university_name:
                employee.university_name = university.name

        for class_ in self.classes_data:
            if class_.university_name == old_university_name:
                class_.university_name = university.name

        for student in self.students_data:
            if student.university_name == old_university_name:
                student.university_name = university.name

        self.view.entry_university_name.delete(0, END)
        self.view.entry_university_city.delete(0, END)
        self.view.entry_university_street.delete(0, END)

        self.university_info()
        self.employee_info()
        self.class_info()
        self.student_info()
        self.view.button_add_university.config(
            text="Dodaj obiekt",
            command=lambda: self.add_university()
        )



############PRACOWNICY############

    def filter_employees(self):
        city_filter = self.view.entry_employee_filter_city.get()
        university_filter = self.view.entry_employee_filter_university.get()

        self.view.listbox_employees.delete(0, END)

        filtered = self.employees_data
        if city_filter:
            filtered = [e for e in filtered if e.city.lower() == city_filter.lower()]
        if university_filter:
            filtered = [e for e in filtered if e.university_name == university_filter]
        
        self.displayed_employees = list(filtered)

        if self.view.selected_category.get() == "Pracownicy":
            for obj, marker_instance in self.markers.items():
                marker_instance.delete()
            self.markers = {}

            for idx, employee in enumerate(self.displayed_employees):
                if hasattr(employee, 'coords') and employee.coords:
                    marker = self.view.map_widget.set_marker(employee.coords[0], employee.coords[1], text=employee.name)
                    self.markers[employee] = marker
                self.view.listbox_employees.insert(idx, f"{employee.name} {employee.city} {employee.street}")
        else:
             for idx, employee in enumerate(self.displayed_employees):
                self.view.listbox_employees.insert(idx, f"{employee.name} {employee.city} {employee.street}")

    def employee_info(self):
        self.filter_employees()

    def add_employee(self) -> None:
        name: str = self.view.entry_employee_name.get()
        city: str = self.view.entry_employee_city.get()
        street: str = self.view.entry_employee_street.get()
        university_name: str = self.view.entry_employee_university.get()
        employee = Employee(name=name, city=city, street=street, university_name=university_name)
        self.employees_data.append(employee)
        self.employee_info()
        self.view.entry_employee_name.delete(0, END)
        self.view.entry_employee_city.delete(0, END)
        self.view.entry_employee_street.delete(0, END)
        self.view.entry_employee_university.delete(0, END)

    def delete_employee(self):
        i = self.view.listbox_employees.index(ACTIVE)
        employee_delete = self.displayed_employees[i]

        if employee_delete in self.markers:
            self.markers[employee_delete].delete()
        
        if employee_delete in self.employees_data:
            self.employees_data.remove(employee_delete)
        
        self.employee_info()

    def edit_employee(self):
        i = self.view.listbox_employees.index(ACTIVE)
        employee = self.displayed_employees[i]

        self.view.entry_employee_name.delete(0, END)
        self.view.entry_employee_city.delete(0, END)
        self.view.entry_employee_street.delete(0, END)
        self.view.entry_employee_university.delete(0, END)
        self.view.entry_employee_name.insert(0, employee.name)
        self.view.entry_employee_city.insert(0, employee.city)
        self.view.entry_employee_street.insert(0, employee.street)
        self.view.entry_employee_university.set(employee.university_name)
        self.view.button_add_employee.config(
            text="Zapisz zmiany",
            command=lambda: self.update_employee(employee)
        )

    def update_employee(self, employee):
        
        employee.name = self.view.entry_employee_name.get()
        employee.city = self.view.entry_employee_city.get()
        employee.street = self.view.entry_employee_street.get()
        employee.university_name = self.view.entry_employee_university.get()
        address = f"{employee.city}, {employee.street}"
        employee.coords = get_coordinates(address)

        if employee in self.markers:
            marker = self.markers[employee]
            marker.set_position(employee.coords[0], employee.coords[1])
            marker.set_text(employee.name)

        self.view.entry_employee_name.delete(0, END)
        self.view.entry_employee_city.delete(0, END)
        self.view.entry_employee_street.delete(0, END)
        self.view.entry_employee_university.delete(0, END)
        self.employee_info()
        self.view.button_add_employee.config(
            text="Dodaj Pracownika",
            command=lambda: self.add_employee()
        )



############KLASY############

    def class_info(self):
        self.view.listbox_classes.delete(0, END)

        for idx, class_ in enumerate(self.classes_data):
            self.view.listbox_classes.insert(idx, f"{class_.name} {class_.university_name}")

        university_names = [university.name for university in self.universities_data]
        self.view.combobox_university_for_class['values'] = university_names

    def add_class(self) -> None:
        name: str = self.view.entry_class_name.get()
        university_name: str = self.view.combobox_university_for_class.get()
        class_ = Class(name=name, university_name=university_name)
        self.classes_data.append(class_)
        self.class_info()
        self.view.entry_class_name.delete(0, END)
        self.view.combobox_university_for_class.set('')
        self.student_info()


    def delete_class(self):
        i = self.view.listbox_classes.index(ACTIVE)
        class_to_delete = self.classes_data[i]
        class_name_to_delete = class_to_delete.name
        university_name_to_delete = class_to_delete.university_name

        self.classes_data.pop(i)
        self.class_info()

        students_to_keep = []
        for student in self.students_data:
            if not (student.class_name == class_name_to_delete and student.university_name == university_name_to_delete):
                students_to_keep.append(student)
        self.students_data = students_to_keep
        self.student_info()

    def edit_class(self):
        i = self.view.listbox_classes.index(ACTIVE)
        class_ = self.classes_data[i]
        self.view.entry_class_name.delete(0, END)
        self.view.entry_class_name.insert(0, class_.name)
        self.view.combobox_university_for_class.set(class_.university_name)
        self.view.button_add_class.config(
            text="Zapisz zmiany",
            command=lambda: self.update_class(i)
        )

    def update_class(self, i):
        class_ = self.classes_data[i]
        old_name = class_.name
        old_university = class_.university_name

        class_.name = self.view.entry_class_name.get()
        class_.university_name = self.view.combobox_university_for_class.get()

        for student in self.students_data:
            if student.class_name == old_name and student.university_name == old_university:
                student.class_name = class_.name
                student.university_name = class_.university_name

        self.view.entry_class_name.delete(0, END)
        self.view.combobox_university_for_class.set('')

        self.class_info()
        self.view.button_add_class.config(
            text="Dodaj Klasę",
            command=lambda: self.add_class()
        )



############UCZNIOWIE############

    def filter_students(self):
        university_filter = self.view.entry_student_filter_university.get()
        class_filter = self.view.entry_student_filter_class.get()

        self.view.listbox_students.delete(0, END)

        filtered = self.students_data
        if university_filter:
            filtered = [s for s in filtered if s.university_name == university_filter]
        if class_filter:
            filtered = [s for s in filtered if s.class_name == class_filter]
        
        self.displayed_students = list(filtered)

        if self.view.selected_category.get() == "Uczniowie":
            for obj, marker_instance in self.markers.items():
                marker_instance.delete()
            self.markers = {}

            for idx, student in enumerate(self.displayed_students):
                if hasattr(student, 'coords') and student.coords:
                    marker = self.view.map_widget.set_marker(student.coords[0], student.coords[1], text=student.name)
                    self.markers[student] = marker
                self.view.listbox_students.insert(idx, f"{student.name} {student.university_name} {student.class_name}")
        else:
            for idx, student in enumerate(self.displayed_students):
                self.view.listbox_students.insert(idx, f"{student.name} {student.university_name} {student.class_name}")

    def student_info(self):
        self.filter_students()
        
        university_names = [university.name for university in self.universities_data]
        self.view.combobox_university_for_student['values'] = university_names
        self.view.entry_student_filter_university['values'] = university_names

    def add_student(self) -> None:
        name: str = self.view.entry_student_name.get()
        address: str = self.view.entry_student_address.get()
        university_name: str = self.view.combobox_university_for_student.get()
        class_name: str = self.view.combobox_class_for_student.get()
        student = Student(name=name, university_name=university_name, class_name=class_name, location=address, position='')
        self.students_data.append(student)
        self.student_info()
        self.view.entry_student_name.delete(0, END)
        self.view.entry_student_address.delete(0, END)
        self.view.combobox_university_for_student.set('')
        self.view.combobox_class_for_student.set('')

    def delete_student(self):
        i = self.view.listbox_students.index(ACTIVE)
        student_to_delete = self.displayed_students[i]

        if student_to_delete in self.markers:
            self.markers[student_to_delete].delete()
        
        if student_to_delete in self.students_data:
            self.students_data.remove(student_to_delete)
        
        self.student_info()

    def edit_student(self):
        i = self.view.listbox_students.index(ACTIVE)
        student = self.displayed_students[i]
        
        self.view.entry_student_name.delete(0, END)
        self.view.entry_student_address.delete(0, END)
        self.view.entry_student_name.insert(0, student.name)
        self.view.entry_student_address.insert(0, student.location)
        self.view.combobox_university_for_student.set(student.university_name)
        self.update_class_combobox(None)
        self.view.combobox_class_for_student.set(student.class_name)
        self.view.button_add_student.config(
            text="Zapisz zmiany",
            command=lambda: self.update_student(student)
        )

    def update_student(self, student):
        
        student.name = self.view.entry_student_name.get()
        student.location = self.view.entry_student_address.get()
        student.university_name = self.view.combobox_university_for_student.get()
        student.class_name = self.view.combobox_class_for_student.get()
        student.coords = get_coordinates(student.location)

        if student in self.markers:
            marker = self.markers[student]
            marker.set_position(student.coords[0], student.coords[1])
            marker.set_text(student.name)

        self.view.entry_student_name.delete(0, END)
        self.view.entry_student_address.delete(0, END)
        self.view.combobox_university_for_student.set('')
        self.view.combobox_class_for_student.set('')

        self.student_info()
        self.view.button_add_student.config(
            text="Dodaj Ucznia",
            command=lambda: self.add_student()
        )

    def update_class_combobox(self, event):
        university_name = self.view.combobox_university_for_student.get()
        class_names = [class_.name for class_ in self.classes_data if class_.university_name == university_name]
        self.view.combobox_class_for_student['values'] = class_names
    
    def update_student_filter_class_combobox(self, event):
        university_name = self.view.entry_student_filter_university.get()
        class_names = [class_.name for class_ in self.classes_data if class_.university_name == university_name]
        self.view.entry_student_filter_class['values'] = class_names

