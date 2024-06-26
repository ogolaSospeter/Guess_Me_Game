import tkinter as tk
import tkinter.messagebox as msgbox
import os
from tkinter import ttk
from datetime import *
import datetime
import random
import PySimpleGUI as sg


class WelcomeScreen:
    def __init__(self):
        self.welcome_window = tk.Tk()
        self.welcome_window.geometry("400x300")
        self.welcome_window.config()
        windowWidth = self.welcome_window.winfo_reqwidth()
        windowHeight = self.welcome_window.winfo_reqheight()
        positionRight = int((self.welcome_window.winfo_screenwidth()/2.4) - (windowWidth/1.5))
        positionDown = int(self.welcome_window.winfo_screenheight()/2 - windowHeight/2)
        self.welcome_window.geometry("+{}+{}".format(positionRight, positionDown))
        self.welcome_window.title("Guess Me Game Welcome Screen")
        message = "Welcome to the Guess Me Game."
        label = tk.Label(self.welcome_window, text=message)
        label.pack(fill=tk.BOTH, expand=0, padx=100, pady=20)
        
        log = "Kindly proceed to Login."
        self.log_label = tk.Label(self.welcome_window, text=log)
        self.log_label.pack(fill=tk.BOTH, expand=0, padx=100, pady=10)
        self.say_hello()
        self.login()
        # start_button = ttk.Button(self.welcome_window, text="Say start", command=self.say_start)
        # start_button.pack(side=tk.TOP, padx=(0, 20), pady=(0, 20))
    
    def say_hello(self):
        message = "Welcome to the Guess Me Game."
        self.label_text = str(message)
        return self.label_text
        
    def login(self):
        login_frame = ttk.Frame(self.welcome_window)
        login_frame.pack(side=tk.TOP)
        self.name_label = ttk.Label(login_frame,text="UserName")
        self.name_label.grid(column=0,row=2,padx=5,pady=5)
        self.name_entry = ttk.Entry(login_frame)
        self.name_entry.grid(column=1,row=2,padx=5,pady=5)
        self.email_label = ttk.Label(login_frame,text="Email")
        self.email_label.grid(column=0,row=3,padx=5,pady=5)
        self.email_entry = ttk.Entry(login_frame)
        self.email_entry.grid(column=1,row=3,padx=5,pady=5)
        self.password_label = ttk.Label(login_frame,text="Password")
        self.password_label.grid(column=0,row=4,padx=5,pady=5)
        self.password_entry = ttk.Entry(login_frame,show="*")
        self.password_entry.grid(column=1,row=4,padx=5,pady=5)

        self.login_button = ttk.Button(login_frame, text="Login" ,padding=5,command=self.validate_login)
        self.login_button.grid(column=0,row=5,columnspan=2,padx=5,pady=5)
        self.exit_button = ttk.Button(login_frame, text="Exit" ,padding=5,command=self.close_login)
        self.exit_button.grid(column=2,row=5,columnspan=2,padx=5,pady=5)

    def validate_login(self):
        username = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if username != "" and email != "" and password != "":
            success_message = f"{username}, You have been successfully Logged in to the system.\nProceed to enjoy the Game."
            msgbox.showinfo("Login Success", success_message)
            self.start_game()  # Automatically start the game after successful login
        else:
            msgbox.showerror("Null Fields!","Kindly fill in all fields to Proceed.!!!")


    def close_login(self):
        confirm = msgbox.askyesno("Confirm exit","Confirm Exit?")
        if confirm:
            self.welcome_window.destroy()
        else:
            pass
        
    def say_start(self):
        option = msgbox.askyesno("Game Start","Do you want to enter the Game?")
        if option:
            msgbox.showinfo("Join the Game","The Game will start shortly...")
            self.start_game()
        else:
            msgbox.showwarning("Game Abort","Game start will abort")

    def start_game(self):
        self.welcome_window.withdraw()  # Close the welcome window
        game = GuessMeGame()
        game.game_window.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox as msgbox
import datetime
import random
import turtle

class GuessMeGame:
    def __init__(self):
        self.game_window = tk.Tk()
        self.game_window.title("Guess Me Game- Game Screen")
        windowWidth = self.game_window.winfo_reqwidth()
        windowHeight = self.game_window.winfo_reqheight()
        positionRight = int((self.game_window.winfo_screenwidth()/2.6) - (windowWidth/1.6))
        positionDown = int(self.game_window.winfo_screenheight()/2 - windowHeight/2)
        self.game_window.geometry("+{}+{}".format(positionRight, positionDown))
        self.questions_frame = None
        self.current_question_index = 0
        self.timer_label = None
        self.timer_seconds = 30
        self.timer_running = False
        self.correct_answers = 0
        self.questions_attempted = 0
        self.attempts = 0

        self.get_attempts()

    def get_attempts(self):
        self.attempts = sg.popup_get_text("Enter the number of attempts", "Attempts", default_text="5",keep_on_top=True)
        if self.attempts is None or self.attempts == "":
            self.attempts = 5
            return self.game_play()
        else:
            self.attempts = int(self.attempts)
            return self.game_play()
        

    def screen_info(self):
        info_frame = ttk.Frame(self.game_window, padding=10)
        info_frame.pack(fill="both", side="top", padx=5, pady=5, expand=1)

        # The player Name
        self.player_name_label = ttk.Label(info_frame, padding=5, text="Player")
        self.player_name_label.grid(row=0, column=0)
        self.player_name_button = ttk.Label(info_frame, background="green", foreground="white", padding=10, width=30, text="John Doe Mwakisu", relief="ridge")
        self.player_name_button.grid(row=1, column=0, padx=7)

        # The Date
        self.current_date_label = ttk.Label(info_frame, padding=5, text="Date")
        self.current_date_label.grid(row=0, column=1)
        current_date = datetime.date.today()
        formatted_date = current_date.strftime("%Y-%m-%d")
        self.current_date_button = ttk.Label(info_frame, background="grey", foreground="white", padding=10, width=30, text=formatted_date, relief="raise")
        self.current_date_button.grid(row=1, column=1, padx=7)

        # The Current time
        self.current_time_label = ttk.Label(info_frame, padding=5, text="Time")
        self.current_time_label.grid(row=0, column=2)
        current_time = datetime.datetime.now().time()
        formatted_time = current_time.strftime("%H:%M:%S")
        self.current_time_button = ttk.Label(info_frame, background="grey", foreground="white", padding=10, width=30, text=formatted_time, relief="raise")
        self.current_time_button.grid(row=1, column=2, padx=7)

        # The player Score
        self.player_score_label = ttk.Label(info_frame, padding=5, text="Player Score")
        self.player_score_label.grid(row=0, column=3)
        self.player_score_button = ttk.Label(info_frame, background="green", foreground="white", padding=10, width=30, relief="raise", text=self.correct_answers)
        self.player_score_button.grid(row=1, column=3, padx=7)

    def game_play(self):
        self.screen_info()  # Call screen_info method upon initialization
        self.questions_frame = ttk.Frame(self.game_window, padding=5)
        self.questions_frame.pack(fill="both", padx=5, pady=5, expand=1)
        self.timer_label = ttk.Label(self.questions_frame, text=f"Time left: {self.timer_seconds} seconds")
        self.timer_label.pack()
        self.canvas = tk.Canvas(self.questions_frame, width=100, height=100)
        self.canvas.pack()
        self.update_progress_bar()
        self.load_next_question()

    def update_progress_bar(self):
        self.canvas.delete("progress")
        progress = 360 * (self.timer_seconds / 30)
        self.canvas.create_arc(5, 5, 95, 95, start=90, extent=-progress, style="arc", outline="green", width=4, tags="progress")

    def load_next_question(self):
        if self.current_question_index < self.attempts:
            self.timer_seconds = 30
            self.timer_running = True
            self.questions_attempted += 1
            self.timer_countdown()
            operators = ['+', '/', '*', '%', '-']
            operator = random.choice(operators)
            num1 = random.randrange(10, 100)
            num2 = random.randrange(10, 100)
            self.qn = f"{num1} {operator} {num2}"
            self.question_frame = ttk.Frame(self.questions_frame, padding=5)
            self.question_frame.pack(fill="both", padx=5, pady=5, expand=1)
            question_index = ttk.Label(self.question_frame, background="blue", foreground="white", text=f"Qn {self.current_question_index + 1}",width=20,padding=7)
            question_index.grid(row=2, column=1, padx=5,rowspan=2)
            question_labl = ttk.Label(self.question_frame, foreground="blue", text=f"Solve the following Arithmetic operation without using a calculator or any electronic device.",padding=7)
            question_labl.grid(row=0, column=2, padx=5,columnspan=2)
            question_label = ttk.Label(self.question_frame, text=f"{self.qn}")
            question_label.grid(row=2, column=2, padx=20)
            question_counter = ttk.Label(self.question_frame,text=f"Qn {self.current_question_index + 1} of {self.attempts}")
            question_counter.grid(row=0, column=4, padx=30,columnspan=2)
            answer_entry = ttk.Entry(self.question_frame)
            answer_entry.grid(row=3, column=2, padx=5)
            next_question_button = ttk.Button(self.question_frame, text="Next", command=lambda: self.process_answer(answer_entry.get()))
            next_question_button.grid(row=4, column=4, padx=50, pady=10)
        else:
            self.timer_running = False
            self.display_results()
    def solve_question(self, question):
        answer = 0
        operator = question.split(" ")[1]
        num1 = question.split(" ")[0]
        num2 = question.split(" ")[2]
        num1 = int(num1)
        num2 = int(num2)
        if operator == "+":
            answer = num1 + num2
        elif operator == "-":
            answer = num1 - num2
        elif operator == "*":
            answer = num1 * num2
        elif operator == "/":
            answer = num1 / num2
        elif operator == "%":
            answer = num1 % num2
        return answer
    

    def timer_countdown(self):
        if self.timer_running and self.timer_seconds > 0:
            self.timer_label.config(text=f"Time left: {self.timer_seconds} seconds")
            self.timer_seconds -= 1
            self.update_progress_bar()
            self.timer_label.after(1000, self.timer_countdown)
        elif self.timer_running and self.timer_seconds == 0:
            self.process_answer(None)

    def process_answer(self, user_answer):
        correct_answer = int(self.solve_question(self.qn))
        if user_answer is not None and user_answer != "":
            user_answer = int(user_answer)
            print("Your answer: ", user_answer)
            print("Correct answer: ", correct_answer)
            if user_answer == correct_answer:
                self.correct_answers += 1
        else:
            print("Your answer: ''")
            print("Correct answer: ", correct_answer)
        self.timer_seconds = 0
        self.current_question_index += 1
        self.question_frame.destroy()
        self.load_next_question()

    def display_results(self):
        self.timer_label.config(text="Test Ended")

        msgbox.showinfo("Test Results", f"Total Questions: {self.questions_attempted}\nCorrect Answers: {self.correct_answers}\nScore: {self.correct_answers * 10} points\nPercentage Pass Rate: {self.correct_answers / self.attempts * 100:.2f}%")
        print(f"Total Questions: {self.questions_attempted}\nCorrect Answers: {self.correct_answers}\nScore: {self.correct_answers * 10} points\nPercentage Pass Rate: {(self.correct_answers /self.attempts) * 100}%")
        self.confirm_restart()
        # sg.popup("Test Results", f"Total Questions: {self.questions_attempted}\nCorrect Answers: {self.correct_answers}\nScore: {self.correct_answers * 10} points\nPercentage Pass Rate: {(self.correct_answers /self.attempts) * 100}%")

    def confirm_restart(self):
        confirm = msgbox.askyesno("Confirm Restart", "Do you want to restart the game?")
        if confirm:
            self.game_window.destroy()
            game = GuessMeGame()
            game.game_window.mainloop()
        else:
            self.confirm_exit()

    def confirm_exit(self):
        confirm = msgbox.askyesno("Confirm Exit", "Do you want to exit the game?")
        if confirm:
            self.game_window.destroy()
        else:
            self.confirm_restart()

def start_Window():
    start_window = tk.Tk()
    start_window.config(height=200,width=300)
    start_window.geometry("300x200")
    start_window.title("Welcome to the Guess Me Game.")
    button = ttk.Button(start_window,text="Start",command= lambda: GuessMeGame.get_attempts)
    button.grid(row=2,column=1,columnspan=2)


start_Window()



















    
# class GuessMeGame:
#     def __init__(self):
#         self.game_window = tk.Toplevel()
#         # self.game_window.geometry("500x700")
#         self.game_window.title("Guess Me Game- Game Screen")
#         self.screen_info()  # Call screen_info method upon initialization
#         self.game_play()

#         self.exit_button = ttk.Button(self.game_window, text="Exit" ,padding=5,command=self.quit_game)
#         self.exit_button.pack(padx=5,pady=5)

#     def screen_info(self):
#         info_frame = ttk.Frame(self.game_window,padding=10)
#         info_frame.pack(fill="both",side="top",padx=5,pady=5,expand=1)

#         #The player Name
#         self.player_name_label = ttk.Label(info_frame,padding=5,text="Player")
#         self.player_name_label.grid(row=0,column=0)
#         self.player_name_button = ttk.Label(info_frame,background="green", foreground="white",padding=10, width=30,text="John Doe Mwakisu",relief="ridge")
#         self.player_name_button.grid(row=1,column=0,padx=7)

#         #The Date
#         self.current_date_label = ttk.Label(info_frame,padding=5,text="Date")
#         self.current_date_label.grid(row=0,column=1)
#         current_date = datetime.date.today()
#         formatted_date = current_date.strftime("%Y-%m-%d")
#         self.current_date_button = ttk.Label(info_frame,background="grey", foreground="white",padding=10, width=30,text= formatted_date,relief="raise")
#         self.current_date_button.grid(row=1,column=1,padx=7)

#         #The Current time
#         self.current_time_label = ttk.Label(info_frame,padding=5,text="Time")
#         self.current_time_label.grid(row=0,column=2)
#         current_time = datetime.datetime.now().time()
#         formatted_time = current_time.strftime("%H:%M:%S")
#         self.current_time_button = ttk.Label(info_frame,background="grey", foreground="white",padding=10, width=30, text= formatted_time,relief="raise")
#         self.current_time_button.grid(row=1,column=2,padx=7)

#         #The player Score
#         self.player_score_label = ttk.Label(info_frame,padding=5, text="Player Score")
#         self.player_score_label.grid(row=0,column=3)
#         self.player_score_button = ttk.Label(info_frame,background="green", foreground="white",padding=10, width=30,relief="raise",text="0")
#         self.player_score_button.grid(row=1,column=3,padx=7)

#     def game_play(self):
#         self.questions_frame =ttk.Frame(self.game_window,padding=5)
#         self.questions_frame.pack(fill="both",padx=5,pady=5,expand=1)
#         questions_label = ttk.Label(self.questions_frame,text=f"Answer the Arithmetic Question Correctly. Each question is worth 10 points.")
#         questions_label.pack(fill="both")

#         operators = ['+','/','*','%','-','>','<','==']

#         self.load_next_question(1)

    
#     def load_next_question(self,n):
#         operators = ['+','/','*','%','-','>','<','==']
#         operator = random.choice(operators)

#         num1 = random.randrange(10,1000)
#         num2 = random.randrange(10,1000)

#         qn = f"{num1} {operator} {num2}"

#         self.question_frame = ttk.Frame(self.questions_frame,padding=5)
#         self.question_frame.pack(fill="both",padx=5,pady=5,expand=1)
#         question_index = ttk.Label(self.question_frame,background="blue",foreground="white",text=f"Qn {n}")
#         question_index.grid(row=0,column=1,padx=5)

#         question_label = ttk.Label(self.question_frame,text=f"{qn}")
#         question_label.grid(row=1,column=1,padx=5)

#         answer_entry = ttk.Entry(self.question_frame)
#         answer_entry.grid(row=2,column=1,padx=5)

#         next_question_button = ttk.Button(self.question_frame,text="Next")
#         next_question_button.grid(row=4,column=4,padx=10, pady=10)



#     def quit_game(self):
#         confirm = msgbox.askyesno("Confirm exit","Confirm Exit?")
#         if confirm:
#             msgbox.showinfo("Game exited.","You have opted out of the game. You can come back any time.")      
#             self.game_window.destroy()
#             main = WelcomeScreen()
#             main.welcome_window.mainloop()
#         else:
#             pass

if __name__ == "__main__":
    # window = WelcomeScreen()
    # window.welcome_window.mainloop()
    window = GuessMeGame()
    window.game_window.mainloop()



# import tkinter as tk
# import tkinter.messagebox as msgbox
# import os
# from tkinter import ttk

# class WelcomeScreen:
#     def __init__(self):
#         super().__init__()
#         self.welcome_window = tk.Tk()
#         self.welcome_window.geometry("400x300")
#         image_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),'..',"assets/"))
#         self.welcome_window.title("Guess Me Game Welcome Screen")
#         # self.iconbitmap(True,image_folder + "/login.PNG")
#         message = "Welcome to the Guess Me Game."
#         label = tk.Label(self.welcome_window, text=message)
#         label.pack(fill=tk.BOTH, expand=0, padx=100, pady=20)
        
#         log = "Kindly proceed to Login."
#         self.log_label = tk.Label(self.welcome_window, text=log)
#         self.log_label.pack(fill=tk.BOTH,expand=0, padx=100, pady=10)
#         self.say_hello()
#         self.login()
#         start_button = ttk.Button(self.welcome_window, text="Say start",
#         command=self.say_start)
#         start_button.pack(side=tk.TOP, padx=(0, 20), pady=(0, 20))
#     def say_hello(self):
#         message = "Welcome to the Guess Me Game."
#         self.label_text = str(message)
#         return self.label_text
        
#     def login(self):
#         login_frame = ttk.Frame(self.welcome_window)
#         login_frame.pack(side=tk.TOP)
#         self.name_label = ttk.Label(login_frame,text="UserName")
#         self.name_label.grid(column=0,row=2,padx=5,pady=5)
#         self.name_entry = ttk.Entry(login_frame)
#         self.name_entry.grid(column=1,row=2,padx=5,pady=5)
#         self.email_label = ttk.Label(login_frame,text="Email")
#         self.email_label.grid(column=0,row=3,padx=5,pady=5)
#         self.email_entry = ttk.Entry(login_frame)
#         self.email_entry.grid(column=1,row=3,padx=5,pady=5)
#         self.password_label = ttk.Label(login_frame,text="Password")
#         self.password_label.grid(column=0,row=4,padx=5,pady=5)
#         self.password_entry = ttk.Entry(login_frame,show="*")
#         self.password_entry.grid(column=1,row=4,padx=5,pady=5)

#         self.login_button = ttk.Button(login_frame, text="Login" ,padding=5,command=self.validate_login)
#         self.login_button.grid(column=0,row=5,columnspan=2,padx=5,pady=5)

#     def validate_login(self):
#         username = self.name_entry.get()
#         email = self.email_entry.get()
#         password = self.password_entry.get()

#         if username != "" and email != "" and password != "":
#             success_message = f"{username}, You have been successfully Logged in to the system.\nProceed to enjoy the Game."
#             msgbox.showinfo("Login Success", success_message)
        
#         else:
#             msgbox.showerror("Null Fields!","Kindly fill in all fields to Proceed.!!!")
        
#     def say_start(self):
#         option = msgbox.askyesno("Game Start","Do you want to enter the Game?")
#         if option:
#             msgbox.showinfo("Join the Game","The Game will start shortly...")
#             self.start_game()
#         else:
#             msgbox.showwarning("Game Abort","Game start will abort")

#     def start_game(self):
#         self.welcome_window.hide()
#         game = GuessMeGame()
#         game.game_window.mainloop()

    
# class GuessMeGame:
#     def __init__(self):
#         super().__init__()
#         self.game_window = tk.Toplevel()
#         self.game_window.geometry("500x700")
#         image_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),'..',"assets/"))
#         self.title("Guess Me Game- Game Screen")

#     def screen_info(self):
#         info_frame = ttk.Frame(self.game_window,padding=10)
#         info_frame.pack(fill="both",side="top",padx=5,pady=5,expand=1)

#         #The player Name
#         self.player_name_label = ttk.Label(info_frame,background="green",padding=5)
#         self.player_name_label.grid(row=0,column=0)
#         self.player_name_button = ttk.Label(info_frame,background="green",padding=5)
#         self.player_name_button.grid(row=1,column=0)

#         #The Date
#         self.current_date_label = ttk.Label(info_frame,background="green",padding=5)
#         self.current_date_label.grid(row=0,column=1)
#         self.current_date_button = ttk.Label(info_frame,background="green",padding=5)
#         self.current_date_button.grid(row=1,column=1)

#         #The Current time
#         self.current_time_label = ttk.Label(info_frame,background="green",padding=5)
#         self.current_time_label.grid(row=0,column=2)
#         self.current_time_button = ttk.Label(info_frame,background="green",padding=5)
#         self.current_time_button.grid(row=1,column=2)

#         #The player Score
#         self.player_score_label = ttk.Label(info_frame,background="green",padding=5)
#         self.player_score_label.grid(row=0,column=3)
#         self.player_score_button = ttk.Label(info_frame,background="green",padding=5)
#         self.player_score_button.grid(row=1,column=3)



# if __name__ == "__main__":
#     window = WelcomeScreen()
#     window.welcome_window.mainloop()