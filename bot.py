import sqlite3

import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, Contact, User, InputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Set up the database connection
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 nickname TEXT NOT NULL ,
                 phone_number TEXT NOT NULL,
                 avatar TEXT)''')
conn.commit()

# Create the Telegram bot
bot = Bot(token='6061105849:AAEyjJiUcaP4xN-aGevEEogoGa61CxaecXo')
dp = Dispatcher(bot)


# Define the registration command
@dp.message_handler(commands=['register'])
async def register(message: Message):
    # Ask the user to send their contact information
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Share Contact', request_contact=True)
    )
    await message.answer("Please share your contact information.", reply_markup=reply_keyboard)


# Handle the user's contact information
@dp.message_handler(content_types=[types.ContentType.CONTACT])
async def handle_contact(message: Message):
    # Get the user data from the contact
    if message.contact:
        contact = message.contact
        username = contact.first_name
        phone_number = contact.phone_number
        user = User.get_current()
        nickname = user.username
        photos = await bot.get_user_profile_photos(user_id=user.id)

        # Check if the user has any profile photos
        if photos.total_count > 0:
            # Get the first photo from the list of profile photos
            photo = photos.photos[0][-1]
            avatar_path = f'avatars/{nickname}.png'
            await photo.download(destination_file=avatar_path)

        else:
            avatar_path = None
        insert_query = "INSERT INTO users (username, nickname, phone_number, avatar) VALUES (?, ?, ?, ?)"
        data = (username, nickname, phone_number, avatar_path)
        cursor.execute(insert_query, data)
        conn.commit()

        # Send a confirmation message to the user
        await message.answer("Thanks for registering!")

        # Redirect the user to their account page
        account_url = "http://localhost:5000/account/" + nickname
        requests.get(account_url)


if __name__ == '__main__':
    executor.start_polling(dp)
