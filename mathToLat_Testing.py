from tkinter import *
root = Tk()

'''
add widgets here
'''


root.title('counting seconds')

# stop_button = Button(root, text='Stop', width=25, command=root.destroy)
# stop_button.pack()


Label(root, text='Day').grid(row=0)
Label(root, text='time').grid(row=1)


day_entry = Entry(root)
time_entry = Entry(root)

day_entry.grid(row=0, column=1)
time_entry.grid(row=1, column=1)

root.mainloop()
