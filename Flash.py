import tkinter as tk
from tkinter import messagebox
import json
import random
import time

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Study App")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.config(bg="#1E1E2F")

        self.flashcards = []  # List to hold flashcards
        self.load_flashcards()  # Load flashcards from file or empty

        # Font and color setup
        self.title_font = ("Helvetica", 20, "bold")
        self.button_font = ("Helvetica", 12)
        self.bg_color = "#1E1E2F"
        self.button_color = "#3E3E5C"
        self.text_color = "#FFFFFF"
        self.highlight_color = "#5C5CFF"

        # Set up UI elements
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(
            self.root,
            text="Flashcard Study App",
            font=self.title_font,
            bg=self.bg_color,
            fg=self.highlight_color,
        )
        title_label.pack(pady=30)

        # Add Flashcard Button
        add_button = tk.Button(
            self.root,
            text="Add Flashcard",
            font=self.button_font,
            bg=self.button_color,
            fg=self.text_color,
            activebackground=self.highlight_color,
            activeforeground=self.bg_color,
            command=self.add_flashcard,
            relief="flat",
        )
        add_button.pack(pady=15, ipadx=10, ipady=5)

        # Start Quiz Button
        start_button = tk.Button(
            self.root,
            text="Start Quiz",
            font=self.button_font,
            bg=self.button_color,
            fg=self.text_color,
            activebackground=self.highlight_color,
            activeforeground=self.bg_color,
            command=self.start_quiz,
            relief="flat",
        )
        start_button.pack(pady=15, ipadx=10, ipady=5)

        # Show Progress Button
        progress_button = tk.Button(
            self.root,
            text="Show Progress",
            font=self.button_font,
            bg=self.button_color,
            fg=self.text_color,
            activebackground=self.highlight_color,
            activeforeground=self.bg_color,
            command=self.show_progress,
            relief="flat",
        )
        progress_button.pack(pady=15, ipadx=10, ipady=5)

    def add_flashcard(self):
        def save_flashcard():
            question = question_entry.get()
            answer = answer_entry.get()

            if question and answer:
                self.flashcards.append(
                    {'question': question, 'answer': answer, 'last_reviewed': time.time(), 'interval': 1}
                )
                self.save_flashcards()
                add_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Both question and answer are required.")

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Flashcard")
        add_window.geometry("400x250")
        add_window.config(bg=self.bg_color)

        question_label = tk.Label(add_window, text="Question:", font=self.button_font, bg=self.bg_color, fg=self.text_color)
        question_label.pack(pady=5)
        question_entry = tk.Entry(add_window, font=self.button_font, width=40)
        question_entry.pack(pady=5)

        answer_label = tk.Label(add_window, text="Answer:", font=self.button_font, bg=self.bg_color, fg=self.text_color)
        answer_label.pack(pady=5)
        answer_entry = tk.Entry(add_window, font=self.button_font, width=40)
        answer_entry.pack(pady=5)

        save_button = tk.Button(
            add_window,
            text="Save Flashcard",
            font=self.button_font,
            bg=self.button_color,
            fg=self.text_color,
            activebackground=self.highlight_color,
            activeforeground=self.bg_color,
            command=save_flashcard,
            relief="flat",
        )
        save_button.pack(pady=15)

    def load_flashcards(self):
        try:
            with open("flashcards.json", "r") as file:
                self.flashcards = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.flashcards = []

    def save_flashcards(self):
        with open("flashcards.json", "w") as file:
            json.dump(self.flashcards, file)

    def start_quiz(self):
        if not self.flashcards:
            messagebox.showwarning("No Flashcards", "Please add some flashcards first.")
            return

        self.quiz_window = tk.Toplevel(self.root)
        self.quiz_window.title("Quiz")
        self.quiz_window.geometry("400x400")
        self.quiz_window.config(bg=self.bg_color)

        self.correct_answers = 0
        self.total_questions = 0
        self.current_flashcard_index = 0
        self.show_next_flashcard()

    def show_next_flashcard(self):
        flashcard = self.flashcards[self.current_flashcard_index]
        self.total_questions += 1

        question_label = tk.Label(
            self.quiz_window, text=flashcard['question'], font=self.button_font, bg=self.bg_color, fg=self.text_color, wraplength=300
        )
        question_label.pack(pady=20)

        answer_entry = tk.Entry(self.quiz_window, font=self.button_font)
        answer_entry.pack(pady=10)

        def check_answer():
            user_answer = answer_entry.get()
            if user_answer.lower() == flashcard['answer'].lower():
                self.correct_answers += 1
            self.current_flashcard_index += 1

            if self.current_flashcard_index < len(self.flashcards):
                self.quiz_window.destroy()
                self.show_next_flashcard()
            else:
                self.quiz_window.destroy()
                self.show_results()

        submit_button = tk.Button(
            self.quiz_window,
            text="Submit Answer",
            font=self.button_font,
            bg=self.button_color,
            fg=self.text_color,
            activebackground=self.highlight_color,
            activeforeground=self.bg_color,
            command=check_answer,
            relief="flat",
        )
        submit_button.pack(pady=10)

    def show_results(self):
        result_window = tk.Toplevel(self.root)
        result_window.title("Quiz Results")
        result_window.geometry("400x200")
        result_window.config(bg=self.bg_color)

        result_label = tk.Label(
            result_window, text=f"Correct Answers: {self.correct_answers}/{self.total_questions}", font=self.button_font, bg=self.bg_color, fg=self.text_color
        )
        result_label.pack(pady=20)

        self.update_flashcards()

    def update_flashcards(self):
        for flashcard in self.flashcards:
            flashcard['interval'] += 1

        self.save_flashcards()

    def show_progress(self):
        correct = sum(1 for card in self.flashcards if card.get('last_reviewed') and card['interval'] > 1)
        total = len(self.flashcards)
        messagebox.showinfo("Progress", f"Correct: {correct}/{total} flashcards reviewed successfully.")


# Create the Tkinter window
root = tk.Tk()
app = FlashcardApp(root)
root.mainloop()
