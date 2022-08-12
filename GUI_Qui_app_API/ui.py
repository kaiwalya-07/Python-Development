from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizIntf:
    def __init__(self, quiz_brain=QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzyfy")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_labl = Label(text="Points:0", fg="black")
        self.score_labl.grid(row=0, column=1)

        self.canvas = Canvas(width=300, heigh=250, bg=THEME_COLOR)
        self.question_text = self.canvas.create_text(150,
                                                     125,
                                                     width=280,
                                                     text="Question",
                                                     fill=THEME_COLOR,
                                                     font=("Arial", 20, "italic"))

        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)
        tr_image = PhotoImage(file="images/true.png")
        self.true_button = Button(image=tr_image, highlightthickness=0, command=self.true_ans)
        self.true_button.grid(row=2, column=0)

        fal_image = PhotoImage(file="images/false.png")
        self.false_button = Button(image=fal_image, highlightthickness=0, command=self.false_ans)
        self.false_button.grid(row=2, column=1)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.canvas.config(bg="white")
            self.score_labl.config(text=f"Points:{self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="Your quiz ends here")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def true_ans(self):
        is_right = self.quiz.check_answer("True")
        self.feedback(is_right)

    def false_ans(self):
        is_right = self.quiz.check_answer("False")
        self.feedback(is_right)

    def feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")

        self.window.after(1000, self.get_next_question)
