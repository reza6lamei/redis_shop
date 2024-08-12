from tkinter import *
from tkinter import ttk
import redis
from tkinter.messagebox import showinfo


class App(Tk):
    def __init__(self):
        self.root = Tk()
        self.root.title('Reza Shop')
        self.rd = redis.Redis(host='localhost', port=6379, password='')

        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        add_menu = Menu(menubar)
        add_menu.add_command(label='add pruduct',command=self.add_product)
        add_menu.add_command(label='Exit',command=self.root.destroy)
        menubar.add_cascade(label="menu",menu=add_menu)

        style = ttk.Style()
        style.theme_use('clam')
    
        self.tree = ttk.Treeview(self.root, column=("name", "price"), show='headings')
        self.tree.heading("name", text="Name")
        self.tree.heading("price", text="Price")
        self.tree.grid(row=2, column=0, sticky='ns')
        scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky='ns')


        Button(self.root, text="Buy", command=self.buy_product).grid(row=0, column=0)
        Button(self.root, text="Refresh", command=self.show).grid(row=0, column=1)
    
    def show(self):
       self.tree.delete(*self.tree.get_children())
       all_keys = self.rd.keys('product_*')
       for key in all_keys:
           name = key.decode('utf-8').split('_')[1]
           price = self.rd.get(key).decode('utf-8')
           self.tree.insert('', 'end', values=(name, price))


    def add_product(self):
        top = Toplevel(self.root)
        name_label = Label(top, text='Name:', font=('bold'), fg='blue', width=5)
        name_label.grid(row=0, column=0)
        name_entry = Entry(top, bg="aquamarine", width=10)
        name_entry.grid(row=0, column=1)

        price_label = Label(top, text='Price:', font=('bold'), fg='blue', width=5)
        price_label.grid(row=1, column=0)
        price_entry = Entry(top, bg='aquamarine', width=10)
        price_entry.grid(row=1, column=1)

        def add():
           name = name_entry.get()
           price = price_entry.get()
           self.rd.set(f'product_{name}', price)
           top.destroy()
           self.show()
        Button(top, text='Add', command=add).grid(row=2, columnspan=2)

    def buy_product(self):
        showinfo(title='Information', message='bought!')
        selected_item = self.tree.selection()[0]
        name = self.tree.item(selected_item, "values")[0]
        self.rd.delete(f'product_{name}')
        self.tree.delete(selected_item)
    def run(self):
        self.root.mainloop()
        
if __name__ == "__main__":
  app = App()
  app.run()