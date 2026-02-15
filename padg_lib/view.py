from tkinter import *
import tkinter.ttk as ttk
import tkintermapview

class MapView:
    def __init__(self, root: Tk):
        self.root = root
        self.root.geometry("1025x850")
        self.root.title("System zarządzania uczelniami")

        self.ramka_zarzadania = Frame(root, height=200)
        self.ramka_mapa = Frame(root)

        self.ramka_zarzadania.grid(row=0, column=0, sticky=N)
        self.ramka_mapa.grid(row=1, column=0)

        self.create_menage_frame(self.ramka_zarzadania)
        self.create_map_frame()

        self.hide_dynamic_frames()
        self.show_frame("Uczelnie")

    def create_menage_frame(self, parent):


        self.create_combobox(parent)

        self.dynamic_frame_container = Frame(parent)
        self.dynamic_frame_container.grid(row=1, column=0, columnspan=1, sticky='nsew')

        self.university_frame = self.create_university_frame(self.dynamic_frame_container)
        self.class_frame = self.create_class_frame(self.dynamic_frame_container)
        self.employee_frame = self.create_employee_frame(self.dynamic_frame_container)
        self.student_frame = self.create_student_frame(self.dynamic_frame_container)


    def create_combobox(self, parent):

        category_frame = Frame(parent)
        category_frame.grid(row=0, column=0, sticky=W)

        Label(category_frame, text="Wybierz kategorię:").grid(row=0, column=0, sticky=W)

        self.selected_category = StringVar()
        categories = ["Uczelnie", "Klasy", "Pracownicy", "Studenci"]

        self.combobox_kategoria = ttk.Combobox(
            category_frame,
            textvariable=self.selected_category,
            values=categories,
            state="readonly"
        )
        self.combobox_kategoria.set(categories[0])
        self.combobox_kategoria.grid(row=0, column=1)



    def create_university_frame(self, parent):
        frame = Frame(parent)

        Label(frame, text="LISTA UCZELNI").grid(row=0, column=0, sticky=W)
        self.listbox_universities = Listbox(frame)
        self.listbox_universities.grid(row=1, column=0)

        self.button_delete_university = Button(frame, text="Usuń Uczelnię")
        self.button_delete_university.grid(row=5, column=0, sticky=W)

        self.button_edit_university = Button(frame, text="Edytuj Uczelnię")
        self.button_edit_university.grid(row=5, column=1, sticky=W)

        formularz = Frame(frame)
        formularz.grid(row=1, column=1, sticky=N)
        Label(formularz, text="Formularz Uczelni").grid(row=0, column=0, columnspan=2)

        Label(formularz, text="Nazwa:").grid(row=1, column=0, sticky=W)
        self.entry_university_name = Entry(formularz)
        self.entry_university_name.grid(row=1, column=1)

        Label(formularz, text="Miasto:").grid(row=2, column=0, sticky=W)
        self.entry_university_city = Entry(formularz)
        self.entry_university_city.grid(row=2, column=1)

        Label(formularz, text="Adres:").grid(row=3, column=0, sticky=W)
        self.entry_university_street = Entry(formularz)
        self.entry_university_street.grid(row=3, column=1)

        self.button_add_university = Button(formularz, text="Dodaj Uczelnię")
        self.button_add_university.grid(row=4, column=0, columnspan=2)

        map_filter_frame = Frame(frame)
        map_filter_frame.grid(row=1, column=2, sticky=N, padx=10)

        Label(map_filter_frame, text="Filtruj (lista i mapa):").grid(row=0, column=0, sticky=W)
        Label(map_filter_frame, text="Miasto:").grid(row=1, column=0, sticky=W)
        self.entry_map_city_filter = Entry(map_filter_frame)
        self.entry_map_city_filter.grid(row=1, column=1, sticky=W, padx=5)
        self.button_show_on_map = Button(map_filter_frame, text="Filtruj")
        self.button_show_on_map.grid(row=2, column=0, sticky=W)
        self.button_reset_university_filter = Button(map_filter_frame, text="Resetuj")
        self.button_reset_university_filter.grid(row=2, column=1, sticky=W, padx=5)

        return frame

    def create_class_frame(self, parent):
        frame = Frame(parent)

        Label(frame, text="LISTA KLAS").grid(row=0, column=0, sticky=W)
        self.listbox_classes = Listbox(frame)
        self.listbox_classes.grid(row=1, column=0)

        self.button_delete_class = Button(frame, text="Usuń Klasę")
        self.button_delete_class.grid(row=5, column=0, sticky=W)

        self.button_edit_class = Button(frame, text="Edytuj Klasę")
        self.button_edit_class.grid(row=5, column=1, sticky=W)

        formularz = Frame(frame)
        formularz.grid(row=1, column=1, sticky=N)
        Label(formularz, text="Formularz Klasy").grid(row=0, column=0, columnspan=2)

        Label(formularz, text="Nazwa:").grid(row=1, column=0, sticky=W)
        self.entry_class_name = Entry(formularz)
        self.entry_class_name.grid(row=1, column=1)

        self.selected_university_for_class = StringVar()
        Label(formularz, text="Uczelnia:").grid(row=2, column=0, sticky=W)
        self.combobox_university_for_class = ttk.Combobox(
            formularz,
            textvariable=self.selected_university_for_class,
            values=[],
            state="readonly"
        )
        self.combobox_university_for_class.grid(row=2, column=1)

        self.button_add_class = Button(formularz, text="Dodaj Klasę")
        self.button_add_class.grid(row=3, column=0, columnspan=2)

        placeholder = Frame(frame, width=200)
        placeholder.grid(row=1, column=2)

        return frame

    def create_employee_frame(self, parent):
        frame = Frame(parent)
        Label(frame, text="LISTA PRACOWNIKÓW").grid(row=0, column=0, sticky=W)
        self.listbox_employees = Listbox(frame)
        self.listbox_employees.grid(row=1, column=0)

        self.button_delete_employee = Button(frame, text="Usuń Pracownika")
        self.button_delete_employee.grid(row=5, column=0, sticky=W)

        self.button_edit_employee = Button(frame, text="Edytuj Pracownika")
        self.button_edit_employee.grid(row=5, column=1, sticky=W)

        formularz = Frame(frame)
        formularz.grid(row=1, column=1, sticky=N)
        Label(formularz, text="Formularz Pracownika").grid(row=0, column=0, columnspan=2)

        Label(formularz, text="Imię:").grid(row=1, column=0, sticky=W)
        self.entry_employee_name = Entry(formularz)
        self.entry_employee_name.grid(row=1, column=1)

        Label(formularz, text="Miasto:").grid(row=2, column=0, sticky=W)
        self.entry_employee_city = Entry(formularz)
        self.entry_employee_city.grid(row=2, column=1)

        Label(formularz, text="Adres:").grid(row=3, column=0, sticky=W)
        self.entry_employee_street = Entry(formularz)
        self.entry_employee_street.grid(row=3, column=1)

        self.selected_university = StringVar()
        Label(formularz, text="Uczelnia:").grid(row=5, column=0, sticky=W)
        self.entry_employee_university = ttk.Combobox(
            formularz,
            textvariable=self.selected_university,
            values=[],
            state="readonly"
        )
        self.entry_employee_university.grid(row=5, column=1)

        self.button_add_employee = Button(formularz, text="Dodaj Pracownika")
        self.button_add_employee.grid(row=6, column=0, columnspan=2)

        map_filter_frame = Frame(frame)
        map_filter_frame.grid(row=1, column=2, sticky=N, columnspan=3, padx=10)

        Label(map_filter_frame, text="Filtruj (lista i mapa):").grid(row=0, column=0, sticky=W)
        
        Label(map_filter_frame, text="Miasto:").grid(row=1, column=0, sticky=W)
        self.entry_employee_filter_city = Entry(map_filter_frame)
        self.entry_employee_filter_city.grid(row=1, column=1, sticky=W, padx=5)
        
        Label(map_filter_frame, text="Uczelnia:").grid(row=2, column=0, sticky=W)
        self.entry_employee_filter_university = ttk.Combobox(
            map_filter_frame,
            values=[],
            state="normal"
        )
        self.entry_employee_filter_university.grid(row=2, column=1, sticky=W, padx=5)

        self.button_filter_employees = Button(map_filter_frame, text="Filtruj")
        self.button_filter_employees.grid(row=3, column=0, sticky=W)
        self.button_reset_employee_filter = Button(map_filter_frame, text="Resetuj")
        self.button_reset_employee_filter.grid(row=3, column=1, sticky=W)

        return frame

    def create_student_frame(self, parent):
        frame = Frame(parent)
        Label(frame, text="LISTA STUDENTÓW").grid(row=0, column=0, sticky=W)
        self.listbox_students = Listbox(frame)
        self.listbox_students.grid(row=1, column=0)

        self.button_delete_student = Button(frame, text="Usuń Studenta")
        self.button_delete_student.grid(row=5, column=0, sticky=W)

        self.button_edit_student = Button(frame, text="Edytuj Studenta")
        self.button_edit_student.grid(row=5, column=1, sticky=W)

        formularz = Frame(frame)
        formularz.grid(row=1, column=1, sticky=N)
        Label(formularz, text="Formularz Studenta").grid(row=0, column=0, columnspan=2)

        Label(formularz, text="Imię:").grid(row=1, column=0, sticky=W)
        self.entry_student_name = Entry(formularz)
        self.entry_student_name.grid(row=1, column=1)

        Label(formularz, text="Adres:").grid(row=2, column=0, sticky=W)
        self.entry_student_address = Entry(formularz)
        self.entry_student_address.grid(row=2, column=1)

        self.selected_university_for_student = StringVar()
        Label(formularz, text="Uczelnie:").grid(row=3, column=0, sticky=W)
        self.combobox_university_for_student = ttk.Combobox(
            formularz,
            textvariable=self.selected_university_for_student,
            values=[],
            state="readonly"
        )
        self.combobox_university_for_student.grid(row=3, column=1)

        self.selected_class_for_student = StringVar()
        Label(formularz, text="Klasa:").grid(row=4, column=0, sticky=W)
        self.combobox_class_for_student = ttk.Combobox(
            formularz,
            textvariable=self.selected_class_for_student,
            values=[],
            state="readonly"
        )
        self.combobox_class_for_student.grid(row=4, column=1)

        self.button_add_student = Button(formularz, text="Dodaj Studenta")
        self.button_add_student.grid(row=5, column=0, columnspan=2)

        map_filter_frame = Frame(frame)
        map_filter_frame.grid(row=1, column=2, sticky=N, padx=10)

        Label(map_filter_frame, text="Filtruj (lista i mapa):").grid(row=0, column=0, sticky=W)
        
        Label(map_filter_frame, text="Uczelnia:").grid(row=1, column=0, sticky=W)
        self.entry_student_filter_university = ttk.Combobox(
            map_filter_frame,
            values=[],
            state="readonly"
        )
        self.entry_student_filter_university.grid(row=1, column=1, sticky=W, padx=5)

        Label(map_filter_frame, text="Klasa:").grid(row=2, column=0, sticky=W)
        self.entry_student_filter_class = ttk.Combobox(
            map_filter_frame,
            values=[],
            state="readonly"
        )
        self.entry_student_filter_class.grid(row=2, column=1, sticky=W, padx=5)

        self.button_filter_students = Button(map_filter_frame, text="Filtruj")
        self.button_filter_students.grid(row=3, column=0, sticky=W)
        self.button_reset_student_filter = Button(map_filter_frame, text="Resetuj")
        self.button_reset_student_filter.grid(row=3, column=1, sticky=W)

        return frame


    def hide_dynamic_frames(self):
        for frame in [self.university_frame, self.class_frame, self.employee_frame, self.student_frame]:
            frame.grid_forget()

    def show_frame(self, frame_name):
        self.hide_dynamic_frames()
        if frame_name == "Uczelnie":
            self.university_frame.grid(row=0, column=0)
        elif frame_name == "Klasy":
            self.class_frame.grid(row=0, column=0)
        elif frame_name == "Pracownicy":
            self.employee_frame.grid(row=0, column=0)
        elif frame_name == "Studenci":
            self.student_frame.grid(row=0, column=0)


    
    def create_map_frame(self):
        # RAMKA MAPY
        self.map_widget = tkintermapview.TkinterMapView(self.ramka_mapa, width=1025, height=650)
        self.map_widget.set_position(52.04, 19.28)
        self.map_widget.set_zoom(6)
        self.map_widget.grid(row=0, column=0)
     