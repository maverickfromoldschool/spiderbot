from tkinter import *
import requests,os,base64,json
from bs4 import BeautifulSoup
from tkinter import messagebox, filedialog, ttk

large_font = ('Verdana', 11)
config = {}

def fetch_url():
    url = address.get()
#    config['images'] = []
#    _images.set(()) # initialized as an empty tuple
    try:
        page = requests.get(url)
    except requests.RequestException as rex:
        _sb(str(rex))
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        images = fetch_images(soup, url)
        if images:
            _images.set(tuple(img['name'] for img in images))
            _sb('Images found: {}'.format(len(images)))
        else:
            _sb('No images found')
        config['images'] = images

def fetch_images(soup, base_url):
    images = []
    for img in soup.findAll('img'):
        src = img.get('src')
        img_url = (
            '{base_url}/{src}'.format(base_url=base_url,src=src))
        name = img_url.split('/')[-1]
        images.append(dict(name=name,url=img_url))
    return images

def save():
    if not config.get('images'):
        _alert('No images to save')
        return
    if _save_method.get() == 'img':
        dirname = filedialog.askdirectory(mustexist=True)
        print(dirname)
        _save_images(dirname)
    else:
         filename = filedialog.asksaveasfilename(
         initialfile='images.json',
         filetypes=[('JSON', '.json')])
         _save_json(filename)

def _save_images(dirname):
    if dirname and config.get('images'):
        for img in config['images']:
            img_data = requests.get(img['url']).content
            filename = os.path.join(dirname, img['name'])
            print(filename)
            with open(filename, 'wb') as f:
                f.write(img_data)
    _alert('Done')

def _save_json(filename):
    if filename and config.get('images'):
        data = {}
    for img in config['images']:
        img_data = requests.get(img['url']).content
        b64_img_data = base64.b64encode(img_data)
        str_img_data = b64_img_data.decode('utf-8')
        data[img['name']] = str_img_data
    with open(filename, 'w') as ijson:
        ijson.write(json.dumps(data))
        _alert('Done')


def _sb(msg):
    status_msg.set(msg)
def _alert(msg):
    messagebox.showinfo(message=msg)



root = Tk()
root.title('Spiderbot')
main_frame = Frame(root,padx=10,pady=10)
#main_frame.grid(row=0,column=0,sticky=(E,W,N,S))
main_frame.pack(side=TOP,fill='both',expand=TRUE)
main_frame.rowconfigure(0,weight=1)
main_frame.columnconfigure(0,weight=1)

url_frame = LabelFrame(main_frame,text='URLs',padx=10,pady=10)
#url_frame.grid(row=0,column=0,sticky=(E,W))
url_frame.pack(side=TOP,fill=X,expand=TRUE)
url_frame.rowconfigure(0,weight=1)
url_frame.columnconfigure(0,weight=1)

address=StringVar(value=large_font)
address.set('http://localhost:8000/')

entry = Entry(url_frame,textvariable=address,font=large_font)
#entry.grid(row=0,column=0,sticky=(N,W,N,S),padx=10,pady=5)
entry.pack(side=LEFT,fill=X,expand=TRUE)
entry.columnconfigure(0,weight=1)
entry.rowconfigure(0,weight=1)

fetch_btn = Button(url_frame,text='Fetch_info',command=fetch_url)
#fetch_btn.grid(row=0,column=1,sticky=W,padx=5)
fetch_btn.pack(side=RIGHT,padx=10)
fetch_btn.rowconfigure(0,weight=1)
fetch_btn.columnconfigure(1,weight=1)


content_frame = LabelFrame(main_frame,text='Content',padx=10,pady=10)
content_frame.pack(side=TOP,fill='both',expand=TRUE)
content_frame.rowconfigure(1,weight=1)
content_frame.columnconfigure(0,weight=1)

_images = StringVar()
list_box = Listbox(content_frame,listvariable=_images)
list_box.pack(side=LEFT,fill='both',expand=TRUE)
list_box.rowconfigure(0,weight=1)
list_box.columnconfigure(0,weight=1)

_scroll_bar = Scrollbar(content_frame,orient=VERTICAL,command=list_box.yview())
_scroll_bar.pack(side=LEFT,padx=10,fill=Y)
_scroll_bar.rowconfigure(0,weight=1)
_scroll_bar.columnconfigure(1,weight=1)
list_box.configure()

_radio_frame = Frame(content_frame)

_radio_frame.pack(side=TOP,padx=30,pady=30)
_radio_frame.rowconfigure(0,weight=1)
_radio_frame.columnconfigure(2,weight=1)

label = Label(_radio_frame,text='choose how to save')
label.pack(side=TOP)
label.rowconfigure(0,weight=1)

label.columnconfigure(0,weight=1)

_save_method = StringVar()
_save_method.set('img')


img_radio_btn = Radiobutton(_radio_frame,text='As images',variable=_save_method,value='img')
img_radio_btn.pack(fill=X,expand=TRUE)
img_radio_btn.rowconfigure(1,weight=1)
img_radio_btn.columnconfigure(0,weight=1)
img_radio_btn.configure(state='normal')

json_radio_btn = Radiobutton(_radio_frame,text='As json',variable=_save_method,value='json')
json_radio_btn.pack()
json_radio_btn.rowconfigure(2,weight=1)
json_radio_btn.columnconfigure(0,weight=1)

_scrape_btn = Button(main_frame,text='SCRAPE',command=save)
_scrape_btn.pack(side=RIGHT,padx=20,pady=10)
_scrape_btn.columnconfigure(0,weight=1)
_scrape_btn.rowconfigure(3,weight=1)

status_msg = StringVar()
status_msg.set('Type the url to scrap..')

status_frame = Frame(root,relief='sunken',padx=5,height=20)
status_frame.pack(side=BOTTOM,fill=X,expand=TRUE)
status_frame.rowconfigure(1,weight=1)
status_frame.columnconfigure(0,weight=1)


status_lbl = Label(status_frame,textvariable=status_msg,anchor=W)
status_lbl.pack(side=BOTTOM,fill=X,expand=TRUE)
status_lbl.columnconfigure(0,weight=1)
status_lbl.rowconfigure(0,weight=1)

root.mainloop()

