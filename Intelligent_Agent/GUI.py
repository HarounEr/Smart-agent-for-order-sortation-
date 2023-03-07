from cgitb import text
from sqlite3 import Row
from tkinter import *
from tkinter import ttk
import tkinter as tk
from turtle import width
import Agent as IA 

ai = IA.agent()



# Main:
root = Tk()
root.title("Autonomous order distribution")
root.geometry("850x570")


# Setting Tabs
tabControl = ttk.Notebook(root)

root.resizable(False,False)

tabControl = ttk.Notebook(root)

orders_tab = ttk.Frame(tabControl)
order_history_tab = ttk.Frame(tabControl)
other_tab = ttk.Frame(tabControl)
#order tab
tabControl.add(orders_tab, text='Orders')
#order history tab
tabControl.add(order_history_tab, text='Order History')
#tab for couriers and manifacturer
tabControl.add(other_tab, text='Other')


tabControl.pack(expand=1, fill="both")
#tab1.configure(background="black")



#############################################
#Order tab
### order tab functions
#open new window function
#defining view components click function

def view_components_click():
    for item in component_treeview.get_children():
        component_treeview.delete(item)
    selected_day = clicked.get().split("Day ")
    day = int(selected_day[1])
    req = ai.readRequirments(day)
    comp1 = req.getComp1()
    comp2 = req.getComp2()
    component_treeview.insert(parent='', index='end', iid=1, text="", values=(comp1[0], comp1[1]))
    component_treeview.insert(parent='', index='end', iid=2, text="", values=(comp2[0], comp2[1]))

def sortOrder():
    selected_day = clicked.get().split("Day ")
    day = int(selected_day[1])
    order_list = ai.sort(day)
    #print(ai.sort(day))

    display_sorted_order_window(order_list)
    update_history_tab()

def selectComp(event):
    componentNameEntry.delete(0, END)
    QuantityNameEntry.delete(0, END)

    selected_item = component_treeview.item(component_treeview.focus())

    component_name = selected_item["values"][0]
    component_quantity = selected_item["values"][1]

    print(component_name)
    print(component_quantity)

    componentNameEntry.insert(0, component_name)
    QuantityNameEntry.insert(0, component_quantity)

def update_quantity():
    selected_item = component_treeview.item(component_treeview.focus())
    component_quantity = selected_item["values"][1]

    new_comp_quantity = QuantityNameEntry.get()

    component_treeview.item(component_treeview.focus(), text='', values=(componentNameEntry.get(),QuantityNameEntry.get()))






def display_sorted_order_window(order_list):
    window = Toplevel(root)
    window.title("Delivery Details")
    window.geometry("590x300")

    first_component_manf = order_list[0][0]
    second_component_manf =order_list[0][1]

    first_component_courier = order_list[1][0]
    second_component_courier = order_list[1][1]

    ttk.Label(window, text="Order Details", font="none 16 bold").grid(row=0, column=2)

    ttk.Label(window, text="First Component:").grid(row=1,column=0)
    ttk.Label(window, text=str(first_component_manf[0][0]), font="none 9 bold").grid(row=1,column=1)

    ttk.Label(window, text="     |").grid(row=1,column=2)

    ttk.Label(window, text="Required quantity:").grid(row=2,column=0)
    ttk.Label(window, text=str(first_component_manf[0][1]), font="none 9 bold").grid(row=2,column=1)

    ttk.Label(window, text="     |").grid(row=2,column=2)

    ttk.Label(window, text="Selected Manufacturers:").grid(row=3,column=0)
    ttk.Label(window, text="     |").grid(row=3,column=2)

    row_column = 3


    for i in range(1,len(first_component_manf)):
        row_column += 1
        str_ = str(first_component_manf[i][0]) + '  [' + str(first_component_manf[i][1]) + ']'
        ttk.Label(window, text=str_ , font="none 9 bold").grid(row=row_column,column=1)
        ttk.Label(window, text="     |").grid(row=row_column,column=2)

    row_column += 1

    ttk.Label(window, text="Selected Couriers:").grid(row=row_column, column=0)
    ttk.Label(window, text="     |").grid(row=row_column,column=2)

    for i in range(1,len(first_component_courier)):
        row_column += 1
        str_ = str(first_component_courier[i][0]) + '  [' + str(first_component_courier[i][1]) + ']'
        ttk.Label(window, text=str_, font="none 9 bold").grid(row=row_column,column=1)
        ttk.Label(window, text="     |").grid(row=row_column,column=2)


    ttk.Label(window, text="Second Component:").grid(row=1,column=4)
    ttk.Label(window, text=str(second_component_manf[0][0]), font="none 9 bold").grid(row=1,column=5)

    ttk.Label(window, text="Required quantity:").grid(row=2,column=4)
    ttk.Label(window, text=str(second_component_manf[0][1]), font="none 9 bold").grid(row=2,column=5)

    ttk.Label(window, text="Selected Manufacturers:").grid(row=3,column=4)
    row_column = 3

    for i in range(1,len(second_component_manf)):
        row_column += 1
        str_ = str(second_component_manf[i][0]) + '  [' + str(second_component_manf[i][1]) + ']'
        ttk.Label(window, text=str_ , font="none 9 bold").grid(row=row_column,column=5)

    row_column += 1

    ttk.Label(window, text="Selected Couriers:").grid(row=row_column,column=4)

    for i in range(1,len(second_component_courier)):
        row_column += 1
        str_ = str(second_component_courier[i][0]) + '  [' + str(second_component_courier[i][1]) + ']'
        ttk.Label(window, text=str_ , font="none 9 bold").grid(row=row_column,column=5)




    window.mainloop()

def update_history_tab(_):
    order_history = IA.select_order_history()

    for i in order_history_treeview.get_children():
        order_history_treeview.delete(i)

    for i in range(0,len(order_history)):
       order_history_treeview.insert(parent='', index='end', text='',values=(order_history[i][1], order_history[i][0], order_history[i][2], order_history[i][3], order_history[i][4]))




# Welcome message
Welcome_label = ttk.Label(orders_tab, text="Welcome to UWE Autonomous order Sorting Agent", font="none 16 bold").pack(pady=5)

main_label = ttk.Label(orders_tab, text="\n", font="none 12").pack()

ChoseADate_Label = Label(orders_tab, text="Select Date to Sort Order: ").place(x=215, y=85)
#drop down menu to select days
options = [ "Select day", "Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7", "Day 8", "Day 9", "Day 10", "Day 11", "Day 12", "Day 13", "Day 14"]
clicked = StringVar()
clicked.set(options[0])
drop = OptionMenu(orders_tab, clicked, *options)
drop.place(x=365, y=79)
#main_label = ttk.Label(orders_tab, text="\n", font="none 12").pack()
#search button to look retieve data after selecting day
Button(orders_tab, text="View Components" ,font="none 10 bold", height=1, command=view_components_click).place(x=487, y=80)
# Component Treeview Frame
component_treeview_frame = Frame(orders_tab)
component_treeview_frame.pack(pady=60)

# Component Treeview Scrollbar
component_scrollbar = Scrollbar(component_treeview_frame)
component_scrollbar.pack(side=RIGHT, fill=Y)

cols = ('Component Name', 'Quantity Needed')
component_treeview = ttk.Treeview(component_treeview_frame, columns=cols, show='headings', yscrollcommand=component_scrollbar.set)
 
for col in cols:
    component_treeview.column(col, anchor=CENTER)
    component_treeview.heading(col, text=col)
    component_treeview.pack()

component_treeview.bind("<ButtonRelease-1>", selectComp)
# Configure scrollbar
component_scrollbar.config(command=component_treeview.yview)




# retrieve component name from table ( to be unchangable ) 
componentName_Label = Label(orders_tab, text="Component Name").place(x=215, y=385)
#componentName_Label.pack(side=LEFT, ipadx=1)
componentName = StringVar()
componentNameEntry = Entry(orders_tab,textvariable=componentName, width=42 )
#making it impossible to change component name
componentNameEntry.bind("<Key>", lambda a: "break")
componentNameEntry.config({"background": "light gray"})

componentNameEntry.place(x=360, y=387)

#retrieve quantity needed and give option to change it
QuantityName_Label = Label(orders_tab, text="Quantity needed").place(x=215, y=418)
component_quantity = StringVar()

QuantityNameEntry = Entry(orders_tab,textvariable=component_quantity, width=42)
QuantityNameEntry.place(x=360, y=420)


#submit button should sort order and open new window with what couriers we are using and so on 

sort_order_btn = Button(orders_tab, text="Sort Order",command = sortOrder,width=26).place(x=214, y=460)
update_btn = Button(orders_tab, text="Update",command = update_quantity,width=26).place(x=424, y=460)

# new window to be opened after clicking on sort order




##############################################
#Order history tab

oder_history_label = Label(order_history_tab, text="Order History",font=(None, 15)).pack()

# Order history Treeview Frame
order_treeview_frame = Frame(order_history_tab)
order_treeview_frame.pack()

order_treeview_frame.bind("<Expose>", update_history_tab)

# Order history Treeview Scrollbar
order_scrollbar = Scrollbar(order_treeview_frame)
order_scrollbar.pack(side=RIGHT, fill=Y,pady=25)

cols1 = ('Day','Component Name','Component Capacity', 'Used Manufacturer','Used Courier')
order_history_treeview = ttk.Treeview(order_treeview_frame, columns=cols1, show='headings', yscrollcommand=order_scrollbar.set )
 
for col in cols1:
    order_history_treeview.column("# 1", anchor=CENTER,width=80)
    order_history_treeview.column(col, anchor=CENTER,width=180)
    order_history_treeview.heading(col, text=col)
    order_history_treeview.pack(pady=25)

# Configure scrollbar
order_scrollbar.config(command=order_history_treeview.yview)


#order_history = IA.select_order_history()

#for i in range(0,len(order_history)):
#    order_history_treeview.insert(parent='', index='end', text='',values=(order_history[i][1], order_history[i][0], order_history[i][2], order_history[i][3], order_history[i][4]))


          
##############################################
#Courier and manufacturer tab

database_tab = ttk.Notebook(other_tab)


courier_tab = ttk.Frame(database_tab)
manufacturer_tab = ttk.Frame(database_tab)

database_tab.add(courier_tab, text = 'Couriers')
database_tab.add(manufacturer_tab, text = 'Manufacturers')

database_tab.pack(padx=15, pady=15, expand = 1, fill = "both")


#Courier treeview
##########################
# Courier Treeview Frame
courier_treeview_frame = Frame(courier_tab)
courier_treeview_frame.pack()

# Component Treeview Scrollbar
courier_scrollbar = Scrollbar(courier_treeview_frame)
courier_scrollbar.pack(side=RIGHT, fill=Y,pady=25)


cols2 = ('Day','Courier', 'Capacity')
courier_treeview = ttk.Treeview(courier_treeview_frame, columns=cols2, show='headings', yscrollcommand=courier_scrollbar.set )
 
for col in cols2:
    courier_treeview.column(col, anchor=CENTER)
    courier_treeview.heading(col, text=col)
    courier_treeview.pack(pady=20)

# Configure scrollbar
courier_scrollbar.config(command=courier_treeview.yview)

db_courier = IA.select_courier()

for i in range(0,len(db_courier)):
    for x in range(1, len(db_courier[i]),2):
        courier_treeview.insert(parent='', index='end', text='',values=(i+1, db_courier[i][x],db_courier[i][x+1]))

#Manufacturer treeview
##########################
# Manufacturer Treeview Frame
manufacturer_treeview_frame = Frame(manufacturer_tab)
manufacturer_treeview_frame.pack()

# Manufacturer Treeview Scrollbar
manufacturer_scrollbar = Scrollbar(manufacturer_treeview_frame)
manufacturer_scrollbar.pack(side=RIGHT, fill=Y,pady=25)

cols3 = ('Component Name','Component Manufacturer', 'Daily Capacity')
manufacturer_treeview = ttk.Treeview(manufacturer_treeview_frame, columns=cols3, show='headings',yscrollcommand=manufacturer_scrollbar.set )
 
for col in cols3:
    manufacturer_treeview.column(col, anchor=CENTER)
    manufacturer_treeview.heading(col, text=col)
    manufacturer_treeview.pack(pady=25)

# Configure scrollbar
manufacturer_scrollbar.config(command=manufacturer_treeview.yview)

db_man = IA.select_manufacturers()

for i in range(0,len(db_man)):
    component = db_man[i][0]
    for x in range(1, len(db_man[i]),2):
        manufacturer_treeview.insert(parent='', index='end', text='',values=(component, db_man[i][x],db_man[i][x+1]))

# Run Gui
root.mainloop()
