import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteEntry
from tkinter import *

# Global variables
Main = None
App = None
table = None

def Start():
    instructions = [
        "LOAD rA, offset(rB)",
        "STORE rA, offset(rB)",
        "BNE rA, rB, offset",
        "CALL label",
        "RET",
        "ADD rA, rB, rC",
        "ADDI rA, rB, imm",
        "NAND rA, rB, rC",
        "DIV rA, rB, rC"
    ]

    global Main
    Main = tk.Tk()
    Main.title("Tomasulo")
    Main.geometry("1000x1000")

    label = tk.Label(Main, text="Welcome to Tomasulo's Simulator", font=('Serif', 16))
    label.pack(pady=20)

    label_2 = tk.Label(Main, text="Please enter instructions from the availble instructions", font=('Serif', 12))
    label_2.pack(pady=10)

    label_2 = tk.Label(Main, text="Available instructions are: \n load rA, offset(rB) \n store rA, offset(rB) \n"
                                  "bne rA, rB, offset \n call label \n ret \n add rA, rB, rC \n addi rA, rB, imm \n"
                                  "nand rA, rB, rC \n div rA, rB, rC" , font=('Serif', 9))
    label_2.pack(pady=10)

    entry_text = tk.Text(Main, font=('Serif', 12), height=10, width=50)
    entry_text.pack(pady=10)

    user_instruction = entry_text.get("1.0", tk.END).split("\n")

    def app_page():
        user_instruction = entry_text.get("1.0", tk.END).split("\n")
        print(user_instruction)

        Main.destroy()

        global App
        App = tk.Tk()
        App.title("Tomasulo")
        App.geometry("1000x1000")

        global table
        table = create_tracing_table(App)

        for inst in user_instruction:
            table.insert("", tk.END, values=(inst, "", "", "", ""))
        App.mainloop()

    btn1 = tk.Button(Main, text="Enter", font=('Arial', 12), command=app_page)
    btn1.pack(pady=20)

    Main.mainloop()

def create_tracing_table(parent):
    table_frame = tk.Frame(parent)
    table_frame.pack(pady=100)

    table = ttk.Treeview(table_frame)
    table['columns'] = ("Instruction", "Issue", "Start Execute", "End Execute", "Write Result", "Commit")
    table.column("#0", width=0, stretch=tk.NO)
    for col in table['columns']:
        table.column(col, anchor=tk.CENTER, width=150)
        table.heading(col, text=col, anchor=tk.CENTER)



    table.pack()

    return table

# def app_page(instruction):
#     Main.destroy()
#
#     global App
#     App = tk.Tk()
#     App.title("Tomasulo")
#     App.geometry("1000x1000")
#
#     global table
#     table = create_tracing_table(App)
#
#
#     for inst in instruction:
#         table.insert("", tk.END, values=(inst, "", "", "", ""))
#
#     App.mainloop()

Start()
