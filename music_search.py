import requests, re
import tkinter as tk

def main():
    gui = GuiWindow()
    txt = gui.txtbox()
    gui.button()
    gui.window.mainloop()



class GuiWindow():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Music Search')
        self.window.geometry('425x300')
        self.window.configure(bg='black')
        self.window.resizable(False,False)
        label = tk.Label(self.window, text='Artist Name',font=('calibri bold',14),bg='black',fg='white')
        label.grid(row=0,column=0,padx=15,pady=15)

        self.o_label1 = tk.Label(self.window,font=('calibri bold',14),fg='red',bg='black')
        self.o_label2 = tk.Label(self.window,font=('calibri bold',12),fg='white',bg='black',justify='left')
        
    
    def txtbox(self):
        self.txt = tk.Entry(self.window,bg='white',fg='black',width=25,font=('calibri bold',12))
        self.txt.grid(row=0,column=1)
        self.txt.focus()
    
    def btn_work(self):
        artist_name = format_name(self.txt.get())
        self.o_label1.config(text='')
        self.o_label2.config(text='')

        if artist_name == None:
            self.o_label1.place(x=25,y=75,anchor='w')
            self.o_label1.config(text='Invalid Artist Name')
        else:
            songs, name = get_songs(artist_name)            
            self.o_label1.place(x=25,y=75,anchor='w')
            #self.o_label2.place_forget()
            
            if songs == None:
                self.o_label1.config(text='Artist not Found')
                
            else:
                name = name.replace('+',' ')
                self.o_label1.config(text=f"{name}'s Trending Songs")
                self.o_label2.place(x=25,y=200,anchor='w')
                self.o_label2.config(text=songs)
            

    def button(self):
        btn = tk.Button(self.window,text='Search',bg='red',fg='white',font=('calibri bold',10),command=self.btn_work)
        btn.place(x=355,y=18)


def format_name(n):
    n = n.strip()
    if match := re.search(r'^[\w ]+$',n):
        n = n.title()
        n = n.replace(' ','+')
        return n
    return None
    
def get_itune_response(name):
    artist_name = name
    get_response = requests.get('https://itunes.apple.com/search?entity=song&media=music&limit=10&term=' + artist_name)
    return get_response.json(), artist_name

def get_songs(name):
    response, artist_name = get_itune_response(name)
    
    if response['resultCount'] == 0:
        return None, None

    songs = ''

    for count, result in enumerate(response['results'], 1):
        songs += f'{count}. {result["trackCensoredName"]}\n'
    
    return songs, artist_name


if __name__ == '__main__':
    main()