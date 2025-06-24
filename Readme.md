
# 📝 Text to .TXT Telegram Bot

## 🌟 Overview
The **Text to .TXT Bot** is a Telegram bot designed to simplify the process of creating, saving, and retrieving text files directly within Telegram. Users can generate `.txt` files by providing a file name and content, with the option to append additional content and customize how it's formatted. The bot also allows users to retrieve their files using unique tokens and view a list of all their generated files. Files are shared in a designated public Telegram channel for easy access.

This bot is perfect for users who need a quick way to create and manage text files, especially for code snippets, notes, or any text-based content, all within the Telegram ecosystem.

---

## 🚀 Features
- **Create `.txt` Files**: Generate text files by specifying a file name and content.
- **Append Content**: Add more content to your file with customizable separators (line gap, no gap, single space, or new line).
- **Code Detection**: Automatically detects if the input resembles code and provides indentation warnings.
- **File Retrieval**: Retrieve files using a unique token generated for each file.
- **File Listing**: View all files associated with your Telegram user ID.
- **Channel Integration**: Files are sent to a specified public Telegram channel with user details and a clickable link.
- **User-Friendly Interface**: Interactive buttons and emojis for a seamless experience.
- **Temporary File Storage**: Uses temporary files for secure and efficient file handling.

---

## 📋 How It Works
The bot operates through a conversational interface with the following steps:

1. **Start the Process**:
   - Use the `/start` command to begin creating a new file.
   - Provide a file name for your `.txt` file.

2. **Add Content**:
   - Enter the initial content for the file.
   - The bot detects if the content resembles code and warns about indentation.

3. **Preview and Edit**:
   - View a preview of the file name and content (up to 200 characters).
   - Choose to:
     - **Done**: Finalize and generate the file.
     - **Add More**: Append additional content.
     - **Cancel**: Abort the process.

4. **Append Content** (Optional):
   - Add more text and choose a separator:
     - **Line Gap**: Adds two newlines (`\n\n`).
     - **No Gap**: Appends directly without spacing.
     - **Single Space**: Adds a single space (` `).
     - **New Line**: Adds a single newline (`\n`).
   - View an updated preview after appending.

5. **Finalize and Share**:
   - The bot generates a `.txt` file and sends it to the user.
   - A unique token is provided for retrieving the file later.
   - The file is also sent to a specified Telegram channel with details like file name, content preview, file size, user name, and a clickable user link.

6. **Retrieve Files**:
   - Use `/getfile {token}` to retrieve a specific file by its token.
   - Use `/getallfiles` to list all files associated with your user ID.

---

## 🎮 Commands
| Command            | Description                              |
|--------------------|------------------------------------------|
| `/start`           | Start creating a new `.txt` file.        |
| `/getfile {token}` | Retrieve a file using its unique token.  |
| `/getallfiles`     | List all files created by the user.      |

---

## 🛠️ Setup and Installation
To deploy the Text to .TXT Bot, follow these steps:

### Prerequisites
- Python 3.7+
- `python-telegram-bot` library (`pip install python-telegram-bot`)
- A Telegram bot token from [BotFather](https://t.me/BotFather)
- A public/private Telegram channel ID or username for sharing files

### Steps
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd text-to-txt-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Bot**:
   - Replace `"BOT-TOKEN"` in the code with your Telegram bot token.
   - Set the `CHANNEL_ID` variable to the ID or username of your public/private Telegram channel (e.g., `@YourChannel` or a numeric ID).

4. **Run the Bot**:
   ```bash
   python bot.py
   ```

5. **Interact with the Bot**:
   - Open Telegram and start a chat with your bot.
   - Use the `/start`, `/getfile`, or `/getallfiles` commands to interact.

---

## 📂 Code Structure
The bot is written in Python using the `python-telegram-bot` library. Key components include:

- **Conversation Handler**: Manages the multi-step process of file creation (states: `NAME`, `CONTENT`, `PREVIEW`, `ADD_CONTENT`, `FINALIZE`).
- **File Handling**: Uses `tempfile.NamedTemporaryFile` for temporary file storage.
- **Code Detection**: Regular expression (`re`) to detect code-like patterns.
- **Token Generation**: Random 10-character tokens using `random` and `string`.
- **Emoji Support**: Enhances user experience with visual cues.
- **User Data Storage**: Stores file metadata in a `user_files` dictionary for retrieval.

---

## 🛡️ Limitations
- **Temporary Files**: Files are stored temporarily and may be deleted by the system. Ensure the `user_files` dictionary persists or implement persistent storage (e.g., a database).
- **Channel Dependency**: Requires a valid Telegram channel ID for sharing files.
- **Indentation Warning**: Code detection is basic and relies on patterns like indentation or keywords.
- **File Size**: Large files may cause issues due to Telegram's file size limits (50 MB for bots).

---

## 🌐 Future Improvements
- Add persistent storage (e.g., SQLite or MongoDB) for `user_files`.
- Support additional file formats (e.g., `.md`, `.py`).
- Enhance code detection with more sophisticated patterns or libraries.
- Add file editing capabilities.
- Implement file deletion or expiration for old files.
- Support private file sharing without a public channel.

---

## 🤝 Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## 📬 Support
For issues or feature requests, please:
- Open an issue on the repository.
- Contact the bot admin via Telegram (if configured).
- Check the Telegram channel for updates.

---

## 📜 License
This project is not licensed.

---

## 🙌 Acknowledgments
- Built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).
- Inspired by the need for quick text file creation in Telegram.
- Thanks to the open-source community for their amazing tools and libraries!

