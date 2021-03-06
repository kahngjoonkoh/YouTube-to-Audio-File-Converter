from sources.mp3_generator import *
from sources.browser import *
import tkinter as tk
import _thread
# TODO: Multithreading

queue = []


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.title("YouTube to Audio File Converter")
        icon = tk.PhotoImage(file="sources/icon.png")
        self.master.iconphoto(False, icon)
        self.master.geometry("500x375")
        self.master.resizable(False, False)
        self.index = 0
        self.pack()

        self.queue_label = tk.Label(self, text="Conversion Queue")
        self.queue_label.grid(row=0, sticky=tk.W, padx=5, pady=(5, 0))

        self.convert_button = tk.Button(self, text="Delete")
        self.convert_button["command"] = self.delete_single
        self.convert_button.grid(row=0, sticky=tk.E, padx=65, pady=(5, 0))

        self.convert_all_button = tk.Button(self, text="Delete All")
        self.convert_all_button["command"] = self.delete_all
        self.convert_all_button.grid(row=0, sticky=tk.E, pady=(5, 0))

        self.queue_listbox = tk.Listbox(self, height=10, width=80)
        self.queue_listbox.grid(row=1)

        self.convert_button = tk.Button(self, text="Add to Queue")
        self.convert_button["command"] = self.add_to_queue
        self.convert_button.grid(row=2, sticky=tk.W, padx=0, pady=(5, 0))

        self.convert_button = tk.Button(self, text="Convert")
        self.convert_button["command"] = self.convert_single
        self.convert_button.grid(row=2, sticky=tk.E, padx=75, pady=(5, 0))

        self.convert_all_button = tk.Button(self, text="Convert All")
        self.convert_all_button["command"] = self.convert_all
        self.convert_all_button.grid(row=2, sticky=tk.E, pady=(5, 0))

        self.link_label = tk.Button(self, text="Edit Link", width=10)
        self.link_label["command"] = self.edit_link
        self.link_label.grid(row=2, sticky=tk.W, padx=150, pady=(5, 0))

        self.output_label = tk.Label(self, text="Output")
        self.output_label.grid(row=4, sticky=tk.W, padx=5, pady=(5, 0))

        self.output_listbox = tk.Listbox(self, height=5, width=80)
        self.output_listbox.grid(row=5)

        self.clear_output_button = tk.Button(self, text="Clear Outputs")
        self.clear_output_button["command"] = self.clear_output_listbox
        self.clear_output_button.grid(row=6, sticky=tk.W, pady=(5, 0))

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.grid(row=6, sticky=tk.E, pady=(5, 0))

    def add_to_queue(self):
        self.add_window = tk.Toplevel(self.master)
        self.add_window.withdraw()
        self.app = AddWindow(self.add_window)

    def convert(self, index=0):
        file_name = queue[index][0]
        link = queue[index][1]

        tempList = file_name.split(" - ")
        artist = tempList[0]
        title = tempList[1]
        if len(tempList) == 3:
            start = file_name.index(" - ")
            space = file_name.index(" - ", start + 1)
            file_name = file_name[:space]
            album = tempList[2]
            if get_mp3(link, file_name, artist, title, album) is True:
                return True
            else:
                return False
        else:
            if get_mp3(link, file_name, artist, title) is True:
                return True
            else:
                return False

    def convert_single(self):
        try:
            index = self.get_selection_index()
            if self.convert(index) is True:
                self.output(f"[~] {queue[index][0]}")
            else:
                self.output(f"[X] {queue[index][0]}")
            self.delete_single(index)
        except IndexError:
            self.output("[!] No selected subject")

    def convert_all(self):
        for i in range(len(queue)):
            if self.convert() is True:
                self.output(f"[~] {queue[0][0]}")
            else:
                self.output(f"[X] {queue[0][0]}")
            self.delete_single(0)
            self.update_queue()

    def output(self, text):
        self.output_listbox.insert(tk.END, text)

    def update_queue(self):
        self.queue_listbox.delete(0, tk.END)
        for item in queue:
            self.queue_listbox.insert(tk.END, item[0])
        self.queue_listbox.see("active")

    def edit_link(self):
        self.edit_window = tk.Toplevel(self.master)
        self.edit_window.withdraw()
        self.app = EditWindow(self.edit_window)

    def get_selection_index(self):
        return self.queue_listbox.curselection()[0]

    def get_selection_item(self):
        return self.queue_listbox.selection_get()

    def clear_output_listbox(self):
        self.output_listbox.delete(0, tk.END)

    def delete_single(self, del_index=None):
        global queue
        try:
            if del_index is None:
                del_index = self.get_selection_index()
            self.queue_listbox.delete(del_index, del_index)
            remove_subject = queue[del_index][0]
            queue.remove(queue[del_index])
            self.output(f"[-] {remove_subject}")
        except IndexError:
            self.output("[!] No selected subject")

    def delete_all(self):
        global queue
        queue = []
        listbox_len = self.queue_listbox.size()
        self.queue_listbox.delete(0, tk.END)
        self.output(f"[-] {listbox_len} item(s)")


class AddWindow(tk.Toplevel):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self)
        self.title("Add to Queue")

        icon = tk.PhotoImage(file="sources/icon.png")
        self.iconphoto(False, icon)
        self.geometry("495x465")
        self.resizable(False, False)

        self.add_label = tk.Label(self, text="Enter name or link of conversion subject")
        self.add_label.grid(row=0, sticky=tk.W, pady=(5, 0))

        self.queue_entry = tk.Text(self, height=25, width=60, padx=5)
        self.queue_entry.grid(row=1)

        self.add_button = tk.Button(self, text="Add")
        self.add_button["command"] = self.add_to_queue
        self.add_button.grid(row=2, sticky=tk.N, ipadx=225, pady=(5, 0))

    def add_to_queue(self):
        raw_text = self.queue_entry.get("1.0", "end-1c")
        temp = raw_text.split('\n')
        try:
            for item in temp:
                if "https://www.youtube.com" in item:
                    queue.append([get_yt_title(item), item])
                else:
                    space = item.index(" ")
                    if ":" in item[:space]:
                        item = item[space + 1:]
                        link = get_yt_link(item)
                        queue.append([item, link])
                    else:
                        link = get_yt_link(item)
                        queue.append([item, link])
            app.output(f"[+] {len(temp)} item(s)")
            app.update_queue()

        except:
            pass

        self.destroy()


class EditWindow(tk.Toplevel):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self)
        self.title("Edit Link")

        icon = tk.PhotoImage(file="sources/icon.png")
        self.iconphoto(False, icon)
        self.geometry("355x60")
        self.resizable(False, False)

        self.edit_label = tk.Label(self, text="Link")
        self.edit_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=(5, 0))

        self.edit_entry = tk.Entry(self, width=50)
        try:
            self.index = app.get_selection_index()
            link = tk.StringVar()
            link.set(queue[self.index][1])
            self.edit_entry["text"] = link

            self.edit_entry.grid(row=1, column=0, padx=5, sticky=tk.W)

            self.edit_button = tk.Button(self, text="Edit")
            self.edit_button["command"] = self.edit_link
            self.edit_button.grid(row=1, column=1, sticky=tk.E, padx=5)
        except IndexError:
            self.destroy()

    def edit_link(self):
        new_link = self.edit_entry.get()
        queue[self.index][1] = new_link
        app.output(f"[*] {app.get_selection_item()}")
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()
