import os
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7533333223:AAEGGlcuHg77VQRIVRz0qawisX2BmPt7nS8"
bot = telebot.TeleBot(TOKEN)

# Sample Quiz Questions
quiz_questions = [
    {"question": "What is the normal range for adult blood pressure?", "options": ["120/80 mmHg", "140/90 mmHg", "160/100 mmHg"], "answer": "120/80 mmHg"},
    {"question": "Which vitamin is essential for blood clotting?", "options": ["Vitamin A", "Vitamin D", "Vitamin K"], "answer": "Vitamin K"},
    {"question": "What is the medical term for low blood sugar?", "options": ["Hyperglycemia", "Hypoglycemia", "Hypertension"], "answer": "Hypoglycemia"},
]

# Start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📚 Study Notes", callback_data="study_notes"))
    markup.add(InlineKeyboardButton("📝 Past Papers", callback_data="past_papers"))
    markup.add(InlineKeyboardButton("🎯 Quiz Mode", callback_data="quiz_mode"))
    bot.send_message(message.chat.id, "Welcome to KMTC Study Bot! Choose an option:", reply_markup=markup)

# Handle Button Clicks
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "quiz_mode":
        send_quiz_question(call.message.chat.id)

# Send a Random Quiz Question
def send_quiz_question(chat_id):
    question = random.choice(quiz_questions)
    markup = InlineKeyboardMarkup()
    for option in question["options"]:
        markup.add(InlineKeyboardButton(option, callback_data=f"answer_{option}_{question['answer']}"))
    bot.send_message(chat_id, question["question"], reply_markup=markup)

# Handle Quiz Answers
@bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"))
def handle_quiz_answer(call):
    _, selected, correct_answer = call.data.split("_", 2)
    if selected == correct_answer:
        bot.send_message(call.message.chat.id, "✅ Correct!")
    else:
        bot.send_message(call.message.chat.id, f"❌ Incorrect! The correct answer is {correct_answer}.")
    send_quiz_question(call.message.chat.id)  # Send next question

print("Bot is running...")
bot.polling()

