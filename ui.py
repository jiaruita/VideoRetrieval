from Tkinter import *
import tkFont
import final_query
import webbrowser


root = Tk()
root.minsize(400,400)
url = ''
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)



title_font = tkFont.Font(weight = tkFont.BOLD)
link_font = tkFont.Font(underline = True)
def goto(event):
    global url
    webbrowser.open_new_tab(url)

    
def exec_search():
    global url
    query = e.get()
    results = final_query.call(query)
    for index, item in enumerate(results):
        if item['description'] == 'none':
            des = ''
        else:
            des = item['description']
        string = item['title'][0] + '\n' + des + '\n'
        title = Label(root, text = item['title'][0] + '\n', font = title_font, width = 100, justify = 'left', anchor = 'w', wraplength = 500)
        
        desc = Label(root, text = des + '\n', width = 100, justify = 'left', anchor = 'w', wraplength = 500)
        
        url = item['url']
        link = Label(root, fg = 'blue', font = link_font, text = url, anchor = 'w')
        link.bind('<ButtonRelease-1>', goto)

        title.pack()
        desc.pack()
        link.pack()
        #t.insert(1.0, item['title'][0] + '\n')
        #button = Button(t, text = 'go', command = goto)
        #t.window_create('2.0', window = button)
        #button.pack()
        

e = Entry(root, text = 'input')

e.pack()

b = Button(root, text = 'search', command = exec_search).pack()




   
root.mainloop()
