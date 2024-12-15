import os
from tempfile import NamedTemporaryFile
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, CallbackContext
from telegram.ext.filters import Text
import re
import random
import string

# Define the states of the conversation
NAME, CONTENT, PREVIEW, ADD_CONTENT, FINALIZE = range(5)

# Emojis to use
emoji_cancel = "❌"
emoji_done = "✅"
emoji_file = "📄"
emoji_discard = "💔"
emoji_start = "🔄"
emoji_support = "💬"  # Support emoji
emoji_add = "➕"  # Add text emoji
emoji_linegap = "⬇️"  # Line gap emoji
emoji_nogap = "🚫"  # No gap emoji
emoji_single_space = "⏳"  # Single space emoji
emoji_newline = "↗️"  # New line emoji

# Channel ID for sending files to a public channel
CHANNEL_ID = "@textdbbyphilox"

# To store the generated files for user retrieval
user_files = {}

# Function to detect if the text looks like code
def is_code(text: str) -> bool:
    # Check if the text contains typical code-like patterns (e.g., indentation, brackets)
    code_pattern = r"(\t|\ {2,})|(\bdef\b|\bclass\b|\bimport\b|\bprint\b)"
    return bool(re.search(code_pattern, text))

# Function to generate a token (random string in upper case)
def generate_token():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

async def start(update: Update, context: CallbackContext):
    # Clear any previous data to prevent old content being used
    context.user_data.clear()

    await update.message.reply_text(
        "Welcome to the Text to .TXT bot! Please provide your file name. 📝",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(emoji_cancel + " Cancel", callback_data='cancel')
        ]])
    )
    return NAME

async def name(update: Update, context: CallbackContext):
    context.user_data['file_name'] = update.message.text
    file_name = context.user_data['file_name']

    # Ask for file content
    await update.message.reply_text(
        f"Got it! What would you like me to save for the content of the file '{file_name}.txt'? 📑",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(emoji_cancel + " Cancel", callback_data='cancel')
        ]])
    )
    return CONTENT

async def content(update: Update, context: CallbackContext):
    context.user_data['file_content'] = update.message.text
    file_name = context.user_data['file_name']
    content = context.user_data['file_content']

    preview_text = f"File Name: {file_name}\n\nContent Preview:\n{content[:200]}..."  # Limiting preview to first 200 chars
    
    # Check if the content looks like code
    if is_code(content):
        note = "\n\n⚠️ **Note:** If you are saving code, please be careful with the indentation."
    else:
        note = ""
    
    # Send preview message
    await update.message.reply_text(
        f"Preview: \n\n{preview_text}{note}",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(emoji_done + " Done", callback_data='done'),
            InlineKeyboardButton(emoji_add + " Add More", callback_data='add_more'),
            InlineKeyboardButton(emoji_cancel + " Cancel", callback_data='cancel')
        ]])
    )
    return PREVIEW

async def add_more(update: Update, context: CallbackContext):
    # Ask for additional content
    await update.callback_query.message.reply_text(
        "Great! Please send the additional content you'd like to add. ✍️",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(emoji_cancel + " Cancel", callback_data='cancel')
        ]])
    )
    return ADD_CONTENT

async def add_content(update: Update, context: CallbackContext):
    # Add the new content to the existing one
    additional_content = update.message.text
    context.user_data['additional_content'] = additional_content

    # Ask the user how they'd like to separate the new content
    await update.message.reply_text(
        "How would you like to separate the new content? \n\n"
        f"{emoji_linegap} - Line Gap\n"
        f"{emoji_nogap} - No Gap\n"
        f"{emoji_single_space} - Single Space\n"
        f"{emoji_newline} - New Line (Half on next line)",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(emoji_linegap, callback_data='line_gap'),
            InlineKeyboardButton(emoji_nogap, callback_data='no_gap'),
            InlineKeyboardButton(emoji_single_space, callback_data='single_space'),
            InlineKeyboardButton(emoji_newline, callback_data='new_line')
        ]])
    )
    return FINALIZE

async def finalize(update: Update, context: CallbackContext):
    gap_choice = update.callback_query.data
    additional_content = context.user_data['additional_content']

    # Choose the separator based on the user's selection
    if gap_choice == 'line_gap':
        separator = "\n\n"
    elif gap_choice == 'no_gap':
        separator = ""
    elif gap_choice == 'single_space':
        separator = " "
    elif gap_choice == 'new_line':
        separator = "\n"  # This will split the content to a new line

    # Append the additional content with the chosen separator
    context.user_data['file_content'] += separator + additional_content
    
    # Show the updated preview with new content
    file_name = context.user_data['file_name']
    content = context.user_data['file_content']
    preview_text = f"File Name: {file_name}\n\nUpdated Content Preview:\n{content[:200]}..."  # Limiting preview to first 200 chars
    
    # Check if the content looks like code
    if is_code(content):
        note = "\n\n⚠️ **Note:** If you are saving code, please be careful with the indentation."
    else:
        note = ""
    
    # Send updated preview message
    await update.callback_query.message.reply_text(
        f"Updated Preview: \n\n{preview_text}{note}",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(emoji_done + " Done", callback_data='done'),
            InlineKeyboardButton(emoji_add + " Add More", callback_data='add_more'),
            InlineKeyboardButton(emoji_cancel + " Cancel", callback_data='cancel')
        ]])
    )
    return PREVIEW

async def done(update: Update, context: CallbackContext):
    file_name = context.user_data['file_name']
    content = context.user_data['file_content']

    # Generate a token for the file (upper case letters and numbers)
    file_token = generate_token()

    # Use NamedTemporaryFile to create a file in a temporary directory
    with NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
        temp_file.write(content)
        temp_file.close()

        # Send the .txt file to the user
        with open(temp_file.name, 'rb') as file:
            await update.callback_query.message.reply_document(document=file, filename=f"{file_name}.txt")

        # Get the user’s full name and their user ID
        user_name = update.callback_query.from_user.full_name
        user_id = update.callback_query.from_user.id

        # Now format the file info for the user
        file_info_user = (
            f"File Name: {file_name}\n\n"
            f"Content Preview: {content[:200]}...\n\n"
            f"Size: {os.path.getsize(temp_file.name)} bytes\n\n"
            f"Use the token `{file_token}` to retrieve this file later. 🔑"
        )

        # Format file info for the channel (with user name and link)
        file_info_channel = (
            f"File Name: {file_name}\n\n"
            f"Content Preview: {content[:200]}...\n\n"
            f"Size: {os.path.getsize(temp_file.name)} bytes\n\n"
            f"User: 𝐏𝐡𝐢𝐥𝐨𝐱 ⏤͟͞xᴏ𝕩「🏴‍☠️」\n"
            f"tg://openmessage?user_id={user_id}\n\n"
            f"Use the token `{file_token}` to retrieve this file later. 🔑"
        )

        # Save the file info in user_files
        user_files[file_token] = {
            'file_name': file_name,
            'file_content': content,
            'file_path': temp_file.name,
            'user_name': user_name,
            'user_id': user_id
        }

        # Send the file to the channel along with the file info (the clickable user link)
        try:
            # Send the file to the channel with the formatted info
            await context.bot.send_message(
                CHANNEL_ID,
                file_info_channel
            )
        except Exception as e:
            print(f"Failed to send message to channel: {e}")

        await update.callback_query.message.reply_text(f"Your file has been generated successfully! {emoji_done}")
        return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.callback_query.message.reply_text(f"File creation canceled. {emoji_cancel}")
    return ConversationHandler.END

async def get_file(update: Update, context: CallbackContext):
    if len(update.message.text.split()) < 2:
        await update.message.reply_text("Usage: /getfile {token}")
        return
    
    token = update.message.text.split()[-1]

    if token in user_files:
        file_info = user_files[token]
        await update.message.reply_document(
            document=open(file_info['file_path'], 'rb'),
            filename=file_info['file_name']
        )
        await update.message.reply_text(
            f"Here is your file '{file_info['file_name']}'.\n\n"
            f"File generated by {file_info['user_name']}."
        )
    else:
        await update.message.reply_text(f"Invalid token! 😞 Please check the token and try again.")

async def get_all_files(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_files_list = [f"{file_info['file_name']} (Token: `{token}`)" for token, file_info in user_files.items() if file_info['user_id'] == user_id]

    if user_files_list:
        await update.message.reply_text(f"Your files:\n\n" + "\n".join(user_files_list))
    else:
        await update.message.reply_text("You don't have any files generated yet. 😞")

def main():
    application = Application.builder().token("7596843854:AAHqw_61u9kasmh0eJHGvV8ddwzX7lXmwsQ").build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(Text(), name)],
            CONTENT: [MessageHandler(Text(), content)],
            PREVIEW: [
                CallbackQueryHandler(done, pattern='^done$'),
                CallbackQueryHandler(add_more, pattern='^add_more$'),
                CallbackQueryHandler(cancel, pattern='^cancel$')
            ],
            ADD_CONTENT: [MessageHandler(Text(), add_content)],
            FINALIZE: [CallbackQueryHandler(finalize)],
        },
        fallbacks=[CallbackQueryHandler(cancel, pattern='^cancel$')],
    )

    application.add_handler(conversation_handler)
    application.add_handler(CommandHandler("getfile", get_file))
    application.add_handler(CommandHandler("getallfiles", get_all_files))

    application.run_polling()

if __name__ == "__main__":
    main()
