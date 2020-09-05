#Functions which perform I/O operations for Warehouse_system.py

#Create ALL list which is list of items in stock (item in stock is also a list with item characteristics)
#If user define another location, add it to locations list
#Released items will be saved in another file

import pickle
from tkinter import *

def add_item(item_data):
    """Input:lisf of item data, saving info into file"""
#Checks if locations_list exist
    try:
        f=open("locations_list","rb")
        locations_list = pickle.load(f)
        f.close()
    except (FileNotFoundError,EOFError):
        error("Nie zdefiniowano żadnej lokalizacji. Utwórz ją, a następnie wprowadź towar na stan.","600x70")
        return None   
#Checks if all_data exist + saving data   
    try:
        file=open("all_data","rb")
        ALL = pickle.load(file)
        file.close()
        if item_data[2] in locations_list:
            if (item_data[0] and item_data[8]):
                try:
                    if int(item_data[8]) > 0:
                        ALL.append(item_data)
                        f=open("locations_list","wb")
                        file=open("all_data","wb")
                        pickle.dump(locations_list,f)
                        pickle.dump(ALL,file)
                        f.close()                
                        file.close()
                    else:
                        error("Parametr 'ilość' musi być liczbą naturalną większą od zera","450x70")
                except ValueError:
                    error("Parametr 'ilość' musi być liczbą naturalną większą od zera","450x70")
            else:
                error("Należy uzupełnić pola 'nazwa' oraz 'ilość'.","400x70")
        else:
            error("Taka lokalizacja nie istnieje. Utwórz nową lokalizację, a następnie dodaj pozycję.","600x70")
    except (FileNotFoundError, EOFError):
        print("Plik z danymi pozycji magazynowych nie istnieje, zostanie utworzony")
        file = open("all_data","wb")
        ALL = []
        pickle.dump(ALL,file)
        file.close()
        add_item(item_data)   
def search_item(criteria,search_entry):
    """Returns results list after searching"""
    try:
        f = open("all_data","rb")
        ALL = pickle.load(f)
        f.close()
    except (FileNotFoundError,EOFError):
        error("Plik z listą towarów nie istnieje. Wprowadź towar na stan, aby utworzyć.","550x70")
    results_list = []
    for item in ALL:
        if search_entry.lower() in str(item[criteria]).lower():
            print(item)
            results_list.append(item)
    if results_list == []:
        error("Nic nie znaleziono","300x70")
    return results_list
def create_location(location_name):
    """Reciveing location_name from entry, adding to locations list"""
    try:
        f = open("locations_list","rb")
        locations_list = pickle.load(f)
        f.close()
        if location_name not in locations_list:       
            locations_list.append(str(location_name))
            f = open("locations_list","wb")
            pickle.dump(locations_list,f)
            f.close()
        else: 
            error("Taka lokalizacja już istnieje. Wprowadź inną nazwę")
    except (IOError, EOFError):
        print("Plik z lokacjami nie istnieje, zostanie utworzony")
        file = open("locations_list","wb")
        locations_list = []
        pickle.dump(locations_list,file)
        file.close()
        create_location(location_name)
def locations_search():
    """Returns list of all locations"""
    try:
        f = open("locations_list","rb")
        locations_list = pickle.load(f)
        f.close()
        return locations_list
    except (FileNotFoundError, EOFError):
        error("Plik z lokacjami nie istnieje lub nie utworzono żadnej lokacji.","450x70")
def edit(selected_item_data,edited_item_data):
    """Add element to ALL with edited_item_data, delete from ALL element with selected_item_data"""
    f = open("all_data","rb")
    ALL = pickle.load(f)
    f.close()
    f = open("all_data","wb")
    ALL.append(edited_item_data)
    ALL.remove(selected_item_data)
    pickle.dump(ALL,f)
    f.close()
def delete_item(selected_item_data):
    f = open("all_data","rb")
    ALL = pickle.load(f)
    f.close()
    f = open("all_data","wb")
    ALL.remove(selected_item_data)
    pickle.dump(ALL,f)
    f.close()   
def release_item(selected_item_data,release_date,release_comments,released_quantity):
    try:
        f=open("released_items","rb")
        released_items = pickle.load(f)
        f.close()
    except (FileNotFoundError,EOFError):
        print("Plik z archiwum wydań nie istnieje, zostanie utworzony")
        f=open("released_items","wb")
        released_items = []
        pickle.dump(released_items,f)
        f.close()   
    if int(released_quantity) == int(selected_item_data[8]):
        #If released quantity is equal to quantity on stock just delete record
        #Then add deleted to released items
        delete_item(selected_item_data)
        selected_item_data.append(release_date)
        selected_item_data.append(release_comments)        
        released_item_data = selected_item_data            
    elif int(released_quantity) < int(selected_item_data[8]):
        #When released quantity lower than quantity on stock just edit item
        edited_item_data = selected_item_data[:]
        edited_item_data[8] = int(edited_item_data[8]) - int(released_quantity)
        edited_item_data[8] = str(edited_item_data[8])
        edit(selected_item_data,edited_item_data)
        #Then add it to released with quantity released_quantity
        selected_item_data[8] = str(released_quantity)
        selected_item_data.append(release_date)
        selected_item_data.append(release_comments)        
        released_item_data = selected_item_data
        released_items.append(released_item_data)                       
    else:
        error("Błędna wartość w polu 'ilość'.","150x70")
    f=open("released_items","wb")
    pickle.dump(released_items,f)
    f.close() 
def release_archive(criteria,search_entry):
    """Returns results list after searching"""
    try:
        f = open("released_items","rb")
        released_items = pickle.load(f)
        f.close()
    except(FileNotFoundError,EOFError):
        error("Plik z archiwum wydań nie istnieje. Przeprowadź wydanie, aby go utworzyć.","530x70")
    results_list = []
    for item in released_items:
        if search_entry.lower() in str(item[criteria]).lower():
            print(item)
            results_list.append(item)

    if results_list == []:
        error("Nic nie znaleziono")
    return results_list
def error(text,size="550x70"):
    """Creating window with 'error' info"""
    root = Tk()
    window = Frame(root)
    root.title("Uwaga!")
    root.geometry(size)
    error_info = Label(root,text=text)
    error_info.pack()
    error_close = lambda : root.destroy() 
    ok_button = Button(root, text="Ok",command=error_close)
    ok_button.pack()
    root.mainloop() 


