import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util
import os
import subprocess
import datetime

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry('1200x520+250+100')
        
        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750,y=300)
        
        self.register_nu__button_main_window = util.get_button(self.main_window, 'register new user', 'gray', self.register, fg = 'black')
        self.register_nu__button_main_window .place(x=750,y=400)
        
        self.webcam_lable = util.get_img_label(self.main_window)
        self.webcam_lable.place(x=10,y=0, width=700, height=500)
        
        self.add_webcam(self.webcam_lable)
        
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        
        self.log_path = './log.txt'
    
    def start(self):
        self.main_window.mainloop()
    
    def login(self):
        unknown_img_path = './.tmp.jpg'
        
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        
        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-5]
        
        if name in ['unknown_person','no_persons_found']:
            util.msg_box('Oops!', 'Unknown user! \n Please register and try again...')
        else:
            util.msg_box('Welcome back!', 'Welcome, {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
                f.close()
        
        os.remove(unknown_img_path)
    
    def register(self):
        self.register_window = tk.Toplevel(self.main_window)
        self.register_window.geometry('1200x520+270+120')
        
        self.accept_button_register_window = util.get_button(self.register_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_window.place(x=750,y=300)
        
        self.try_again_button = util.get_button(self.register_window, 'Try again', 'red', self.try_again_register)
        self.try_again_button.place(x=750,y=400)
        
        self.capture_label = util.get_img_label(self.register_window)
        self.capture_label.place(x=10,y=0, width=700, height=500)
        
        self.add_img_to_label(self.capture_label)
        
        self.entry_text_register_new_user = util.get_entry_text(self.register_window)
        self.entry_text_register_new_user.place(x=750,y=150)
        
        self.text_label_register_new_user = util.get_text_label(self.register_window,'Please, input username')
        self.text_label_register_new_user.place(x=750,y=70)
        
    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        
        self.register_new_user_capture = self.most_recent_capture_arr.copy()
        
    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)
        
        util.msg_box('Success','User registered successfully !')
        
        self.register_window.destroy()
        
    def try_again_register(self):
        self.register_window.destroy()
    
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        
        self._label = label
        self.process_webcam()
    
    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        
        self._label.after(20, self.process_webcam)
        

if __name__ == '__main__':
    app = App()
    app.start() 