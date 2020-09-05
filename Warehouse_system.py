#Simple system dedicated to warehouse work - created just for practise

#Functions:
#Main window
    #Create class for main window (based on class frame)
        #Widgets:
            #On top label with short description
            #Below buttons for all functions
            #After click on function button shows new window, description below
#Acceptance into stock
    #Create class for acceptance into stock (based on class frame)
    #Create label+entry for each feature to set by user
    #Create buttons 'accept' and 'abort'
        #Accept button saves new item in stock
        #Abort destroying window
#Release from stock
    #Releasing will be able to do from search engine
        #Details:
        #Create class (window) for release from stock
        #Entry+labels - date of release, comments to release
        #Accept button saving released item data (all data + date of release + comment) in new file
        #Abort destroy window
#Change characteristics item in stock
    #Item characteristics : name, date of acceptance,location, weight, sizes(weight,length,depth), value, quantity
    #Each feature is editable (label+entry), each item and its description will be saved in file
    #Characteristics will be changed via browser  
        #Create popup menu 
        #Bind popup menu to leftclick 
        #Popup menu options:
            #Edit - create class based on accept into stock class
            #Insert to entries item data from selected by user item in search engine
            #after hit accept, save new data into file, delete old data from file
            
            #Delete - get data from selected by user item from search engine
            #Delete it from file 
            #Before delete show "are you sure?" window
            
            #Release from stock - create class based on Frame
            #In window should be entry for release date and textbox for comments to release
            #After accept add this data to standard item data list, then add to released items list
            #delete released item from file             
#Add location
     #Create class for creating location window (based on class frame)
     #Label+entry for enter new location name
     #create separate list for locations only
     #if user enter location that doesn't exist in locations list, show info in separate window
#Search item in stock
    #Create class for browser (based on class frame)
    #Search by each of characteristics
    #Create widgets :
        #Radiobuttons on top, searching criteria + 'all'
        #Entry below
        #On bottom list of search result in treeview widget (ttk)
    #In search engine user can edit item,delete item and release from stock (look change characteristics item in stock)

#Functions which operates on files (all items in stock data, locations, released items) write in module

from tkinter import *
import tkinter.ttk as ttk
import IOFunctions as data

class Main_window(Frame):
    """Main window with all widgets"""
    def __init__(self,master):
        super(Main_window,self).__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """All widgets"""
    #Label+Buttons in main window - main program functions
        Label(self, text="Wybierz funkcję:").pack(fill=X)
        main_menu_buttons_info=[("Wprowadź na stan magazynowy",self.into_stock),
                                ("Utwórz lokalizację",self.create_location),
                                ("Lista lokacji",self.locations),
                                ("Wyszukaj pozycję",self.search_item),
                                ("Archiwum wydań",self.released_items),
                                ("Wyjdź",self.close)]        
        for text,command in main_menu_buttons_info:
            Button(self,
                   text=text,
                   command=command
            ).pack(fill=X)
    
    #Functions attached to buttons in main window
    def into_stock(self):
        """Create window for acceptance into stock option"""
        self.into_stock_root = Tk()
        self.window = Accept_into_stock(self.into_stock_root)
        self.into_stock_root.title("Wprowadź na stan magazynowy")
        self.into_stock_root.geometry("350x500")
        self.master.withdraw()
        self.into_stock_root.mainloop()
        root.withdraw()

    def create_location(self):
        """Window for create location"""
        self.create_location_root = Tk()
        self.window = Create_location(self.create_location_root)
        self.create_location_root.title("Wprowadź na stan magazynowy")
        self.create_location_root.geometry("350x150")
        self.master.withdraw()
        self.create_location_root.mainloop()

    def locations(self):
        """Window with locations list"""
        self.locations_root = Tk()
        self.window = Locations(self.locations_root)
        self.locations_root.title("Lista lokacji")
        self.locations_root.geometry("350x300")
        self.locations_root.mainloop()        

    def search_item(self):
        """Create window for browser"""   
        self.search_item_root = Tk()
        self.window = Search_item(self.search_item_root)
        self.search_item_root.title("Wyszukaj pozycję")
        self.search_item_root.geometry("1300x450")
        self.master.withdraw()
        self.search_item_root.mainloop()

    def released_items(self):
        """Released items search engine"""
        self.released_items_root = Tk()
        self.window = Released_items(self.released_items_root)
        self.released_items_root.title("Archiwum wydań")
        self.released_items_root.geometry("1200x550")
        self.master.withdraw()
        self.released_items_root.mainloop()        
    
    def close(self):
        """Closing main window"""
        self.master.destroy()

class Accept_into_stock(Frame):
    """Acceptance into stock window with all widgets"""
    def __init__(self,master):
        super(Accept_into_stock,self).__init__(master)
        self.pack()
        self.create_widgets()
    def create_widgets(self):
        """Create all widgets in window"""
    #Create entries+labels for all of item data 
        self.entries = []
        self.entry_list = ["Nazwa","Data przyjęcia","Lokalizacja",
                      "Waga","Długość","Szerokość",
                      "Głębokość","Wartość","Ilość"]
        for title in self.entry_list:
            Label(self,text=title).pack()
            title = Entry(self)
            title.pack()
            self.entries.append(title)
    
    #Create buttons accept and abort     
        abort = None
        accept = None
        buttons_list = [["Akceptuj",accept, self.accept],["Anuluj",abort, self.abort]]
        for title in buttons_list:
            title[1] = Button(self,
                         text=title[0],
                         command = title[2])
            title[1].pack()
       
    def accept(self):
        """Gets data from labels, saves into file using add_item from Database.py"""
        item_info = []
        for entry in self.entries:
            info = entry.get()
            item_info.append(info)
        data.add_item(item_info)
        self.master.destroy()  
        root.deiconify()
    def abort(self):
        """Closing window after hit "abort" button"""
        self.master.destroy()
        root.deiconify()
            
class Search_item(Frame):
    """Class for search engine window"""
    def __init__(self,master):
        super(Search_item,self).__init__(master)
        self.grid()
        self.create_widgets()
    
    def create_widgets(self):
        """All widgets in window"""
        Label(self, text="Kryteria wyszukiwania:").grid(row=0,column=4)
    #Radiobuttons for all searching criteria
        self.radiobutton_data = [("Nazwa",0),("Data przyjęcia",1),("Lokalizacja",2),
                      ("Waga",3),("Długość",4),("Szerokość",5),
                      ("Głębokość",6),("Wartość",7),("Ilość",8)]
        self.criteria = IntVar(self)
        self.criteria.set(0)
        for text,value in self.radiobutton_data:
            Radiobutton(self,
                        text=text,
                        variable=self.criteria,
                        value=value,
                        ).grid(row=1,column=value)
    #Search key entry
        self.search_entry = Entry(self)
        self.search_entry.grid(row=2,column=4)
    #Treeview of search results
        #Search result label
        Label(self,text="Wyniki wyszukiwania:").grid(row=3,column=4)
        #Create treeview widget
        self.results_tree = ttk.Treeview(self)
        self.results_tree.grid(column=1,row=4,columnspan=9,rowspan=4)
        #Columns
        self.results_tree["columns"]=("Nazwa","Data przyjęcia","Lokalizacja",
                                 "Waga","Długość","Szerokość",
                                 "Głębokość","Wartość","Ilość")
        #Format columns
        self.columns_names =(("Nazwa"),("Data przyjęcia"),("Lokalizacja"),
                       ("Waga"),("Długość"),("Szerokość"),
                       ("Głębokość"),("Wartość"),("Ilość"))     
        self.results_tree.column("#0",width=0,minwidth=0)
        for name in self.columns_names:
            self.results_tree.column(name, width=130,minwidth=90)
        #Column headings
        self.results_tree.heading("#0",text="Nazwa")        
        for name in self.columns_names:
            self.results_tree.heading(name, text=name,anchor=W)           
    #Buttons 'search' and 'abort'
        abort = None
        search = None
        buttons_list = [["Wyszukaj",search, self.search],["Anuluj",abort, self.abort]]
        for title in buttons_list:
            title[1] = Button(self,
                         text=title[0],
                         command = title[2])
            title[1].grid(column=4)
    
    #Code after hit 'search' button
    def search(self):
        """Insert search results to listbox"""
        #Clear treeview
        for i in self.results_tree.get_children():
            self.results_tree.delete(i)
        #Get results list from module, insert to treeview
        results_list = data.search_item(self.criteria.get(),self.search_entry.get()) 
        row_index = 1
        for item in results_list:
            self.results_tree.insert("",row_index,values=(item))
            row_index +=1
        #Call popup_menu
        self.popup_menu()           
        
    def popup_menu(self):
        def edit():
            #Get item index in treeview
            focused_item = self.results_tree.focus()
            #Get data from columns in focused item
            focused_item_data = self.results_tree.set(focused_item)
            #From focued item data dictionary get only values to list selected_item_data
            selected_item_data = []
            for column_name in self.columns_names:
                value = focused_item_data.get(column_name)
                selected_item_data.append(value)
            #Create window based on class Accept_into_stock,send selected_item_data to Edit_item class          
            self.edit_window_root = Tk()
            self.edit_window = Edit_item(self.edit_window_root,selected_item_data,self.master)
            self.edit_window_root.title("Edytuj dane towaru")
            self.master.withdraw()
            self.edit_window_root.mainloop  
            
        def delete():
            #Get item index in treeview
            focused_item = self.results_tree.focus()
            #Get data from columns in focused item
            focused_item_data = self.results_tree.set(focused_item)
            #From focued item data dictionary get only values to list selected_item_data
            selected_item_data = []
            for column_name in self.columns_names:
                value = focused_item_data.get(column_name)
                selected_item_data.append(value)
            #Create window with 2 buttons - 'accept' and 'abort'          
            self.delete_window_root = Tk()
            self.delete_window = Delete_item(self.delete_window_root,selected_item_data,self.master)
            self.delete_window_root.title("Usuń towar")
            self.master.withdraw()
            self.delete_window_root.mainloop  
                        
        def release():
            #Get item index in treeview
            focused_item = self.results_tree.focus()
            #Get data from columns in focused item
            focused_item_data = self.results_tree.set(focused_item)
            #From focused item data dictionary get only values to list selected_item_data
            selected_item_data = []
            for column_name in self.columns_names:
                value = focused_item_data.get(column_name)
                selected_item_data.append(value)
            #Create window with entry release date and texbox with comments         
            self.release_window_root = Tk()
            self.release_window = Release_item(self.release_window_root,selected_item_data,self.master)
            self.release_window_root.geometry("300x300")
            self.release_window_root.title("Wydaj z magazynu")
            self.master.withdraw()
            self.release_window_root.mainloop 
    
    #Create Menu widget
        self.menu = Menu(self.results_tree, tearoff=0)
        self.menu.add_command(label = "Edytuj", command = edit)
        self.menu.add_command(label = "Usuń", command = delete)
        self.menu.add_command(label="Wydaj z magazynu",command= release)
        def popup(event):
            self.menu.post(event.x_root,event.y_root)
        self.results_tree.bind("<Button-3>",popup)
         
    def abort(self):
        """Closing window after hit "abort" button"""
        self.master.destroy()
        root.deiconify()          

class Create_location(Frame):
    """Class for creating location window"""
    def __init__(self,master):
        super(Create_location,self).__init__(master)
        self.pack()
        self.create_widgets() 
    def create_widgets(self):
        """All widgets in window"""
    #Entry + label for enter location name
        Label(self,text="Wprowadź nazwę nowej lokalizacji:").pack()
        self.location_name_entry = Entry(self)
        self.location_name_entry.pack()
    #Accept/abort buttons
        accept = Button(self,
                        text="Akceptuj",
                        command=self.accept)
        accept.pack()
        abort = Button(self,
                       text="Anuluj",
                       command=self.abort)
        abort.pack()
    def accept(self):
        """Creating sublist in ALL list named as string in location_name_entry"""
        data.create_location(self.location_name_entry.get())
        self.master.destroy()
        root.deiconify()      
    def abort(self):
        """Destroying window"""
        self.master.destroy()
        root.deiconify()

class Locations(Frame):
    """Class for locations search engine"""
    def __init__(self,master):
        super(Locations,self).__init__(master)
        self.pack()
        self.create_widgets()
    def create_widgets(self):
    #Label+listbox with all locations
        Label(self,text="Utworzone lokacje:").pack()
        locations = Listbox(self)
        locations.pack()
    #Refresh and abort buttons    
        refresh_button = Button(self,
                         text="Odśwież",
                         command=lambda:self.load_locations(locations))
        abort_button = Button(self,
                       text="Anuluj",
                       command= lambda:self.master.destroy())
        refresh_button.pack()
        abort_button.pack()    
    def load_locations(self,locations):
        locations_list = data.locations_search()
        locations.delete(0,END)        
        print(locations_list)
        for location in locations_list:                   
            locations.insert(END,location)

class Released_items(Search_item): 
    def create_widgets(self):
        """All widgets in window - copy of create widgets in Search item but added 2 more columns"""
    #Radiobuttons for all searching criteria        
        Label(self, text="Kryteria wyszukiwania:").grid(column=0,row=0,columnspan=11)
        self.radiobutton_data = [("Nazwa",0),("Data przyjęcia",1),("Lokalizacja",2),
                      ("Waga",3),("Długość",4),("Szerokość",5),
                      ("Głębokość",6),("Wartość",7),("Ilość",8),("Data wydania",9),("Komentarz",10)]
        self.criteria = IntVar(self)
        self.criteria.set(0)
        for text,value in self.radiobutton_data:
            Radiobutton(self,
                        text=text,
                        variable=self.criteria,
                        value=value,
                        ).grid(column=value,row=1)
        self.search_entry = Entry(self)
        self.search_entry.grid(column=0,row=2,columnspan=11)
    #Treeview of search results
        #Search result label
        Label(self,text="Wyniki wyszukiwania:").grid(column=0,row=3,columnspan=11)
        #Create treeview widget
        self.results_tree = ttk.Treeview(self)
        self.results_tree.grid(column=0,row=4,columnspan=11)
        #Columns
        self.results_tree["columns"]=("Nazwa","Data przyjęcia","Lokalizacja",
                                 "Waga","Długość","Szerokość",
                                 "Głębokość","Wartość","Ilość","Data wydania","Komentarz")
        #Format columns
        self.columns_names =(("Nazwa"),("Data przyjęcia"),("Lokalizacja"),
                       ("Waga"),("Długość"),("Szerokość"),
                       ("Głębokość"),("Wartość"),("Ilość"),("Data wydania"),("Komentarz"))     
        self.results_tree.column("#0",width=0,minwidth=0)
        for name in self.columns_names:
            self.results_tree.column(name, width=100,minwidth=90)
        #Column headings
        self.results_tree.heading("#0",text="Nazwa")        
        for name in self.columns_names:
            self.results_tree.heading(name, text=name,anchor=W)           
    #Buttons 'search' and 'abort'
        abort = None
        search = None
        buttons_list = [["Wyszukaj",search, self.search],["Anuluj",abort, self.abort]]
        for title in buttons_list:
            title[1] = Button(self,
                         text=title[0],
                         command = title[2])
            title[1].grid(column=0,columnspan=11)        
    def search(self):
        """Insert search results to listbox - changed source of data to data.release_archive"""
        #Clear treeview
        for i in self.results_tree.get_children():
            self.results_tree.delete(i)
        #Get results list from module, insert to treeview
        results_list = data.release_archive(self.criteria.get(),self.search_entry.get()) 
        row_index = 1
        for item in results_list:
            self.results_tree.insert("",row_index,values=(item))
            row_index +=1
        #Call popup_menu
        self.popup_menu()
    def popup_menu(self):
        pass #can be developed later
    def abort(self):
        """Destroy window"""
        self.master.destroy()
        root.deiconify()  

class Edit_item(Accept_into_stock):
    """Window for edit selected item"""
    def __init__(self,master,selected_item_data,search_item_root):
        super(Edit_item,self).__init__(master)
        self.search_item_root = search_item_root
        self.selected_item_data = selected_item_data
        self.insert_data()
        
    def insert_data(self):
        """Inserts selected_item_data to entries in window"""
        selected_item_data_index = 0
        for entry in self.entries:
            entry.insert(0,self.selected_item_data[selected_item_data_index])
            selected_item_data_index += 1
    
    def read_data(self):
        """Create list edited_item_data taken from entries"""
        edited_item_data = []
        for entry in self.entries:
            edited_item_data.append(entry.get())
        return edited_item_data
    
    def accept(self):
        """Recieve selected_item_data and edited_item_data, call data.edit() to save into file"""
        #selected_item_data called by self. 
        print("Selected_item_data w klasie Edit_item", self.selected_item_data) #DELETE THIS AFTER TESTING
        #edited_item_data called by read_data()
        edited_item_data = self.read_data()
        print("Edited item_data w klasie Edit_item:", edited_item_data)
        #call data.edit - saving to file, delete old item
        data.edit(self.selected_item_data,edited_item_data)
        self.master.destroy()
        self.search_item_root.deiconify()
        
    def abort(self):
        """Destroy master root"""
        self.master.destroy()
        self.search_item_root.deiconify()

class Delete_item(Frame):
    """Window for delete item"""
    def __init__(self,master,selected_item_data,edit_window_root):
        super(Delete_item,self).__init__(master)
        self.edit_window_root = edit_window_root
        self.selected_item_data = selected_item_data
        self.pack()
        self.create_widgets()
    
    def create_widgets(self):
        """Create label+buttons accept and abort"""
        Label(self,text="Wpis zostanie całkowicie usunięty. Kontynuować ?").pack()
        Button(self,text="Akceptuj",command = self.accept).pack()
        Button(self,text="Anuluj",command=self.abort).pack()
    
    def accept(self):
        """Call function from module which delete selected item data"""
        data.delete_item(self.selected_item_data)
        self.master.destroy()
        self.edit_window_root.deiconify()
    def abort (self):
        """Destroy window"""
        self.master.destroy()    
        self.edit_window_root.deiconify()

class Release_item(Frame):
    """Window for release item from stock"""
    def __init__(self,master,selected_item_data,search_window_root):
        super(Release_item,self).__init__(master)
        self.search_window_root = search_window_root
        self.selected_item_data = selected_item_data
        self.pack()
        self.create_widgets()
    
    def create_widgets(self):
        """Creates widgets - labels + textbox for release comments and entry for release date"""
    #Enter release_date + Label
        Label(self,text="Wprowadź datę wydania:").pack()
        self.release_entry = Entry(self)
        self.release_entry.pack()

    #Enter quantity : label+entry
        Label(self,text="Ilość:").pack()
        self.released_quantity_entry = Entry(self)
        self.released_quantity_entry.pack()
        
    #Enter release_comments + Label
        Label(self,text="Uwagi:").pack()
        self.release_comments = Text(self, height=5,width=20)
        self.release_comments.pack()
        
    #Accept, abort buttons
        accept = Button(self,text="Akceptuj",command = self.accept)
        accept.pack()
        abort = Button(self,text="Anuluj",command = self.abort)
        abort.pack()
        
    def accept(self):
        """Gets data from widgets, calls function for release from module"""
        #Get release_date from entry
        release_date = self.release_entry.get()
        #Get release_comments from textbox
        release_comments = self.release_comments.get("1.0",END)
        #Get released_quantity from entry
        released_quantity = self.released_quantity_entry.get()
        #Call data.release_item
        data.release_item(self.selected_item_data,release_date,release_comments,released_quantity)
        #Destroy window
        self.master.destroy()
        self.search_window_root.deiconify()
        print("Dane z wydania:", release_date,release_comments) #DELETE IT
    
    def abort(self):
        """Destroy window"""
        self.master.destroy()
        self.search_window_root.deiconify()     


#MAINLOOP
root = Tk()
main = Main_window(root)
root.title("Warehouse system")
root.geometry("400x250")
root.mainloop()

