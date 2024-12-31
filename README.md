#### Simple tg bot that uses the GigaChat AI to interact with users through Telegram. The bot answers questions using the GigaChat model and saves the conversation history in a PostgreSQL database.
Stack: Python, aiogram, gigachat, SQLAlchemy, Alembic

## Commands
- `/start` — welcome message
- `/help` — commands info
- `/clear` — clears user conversation history with the bot

## Run with Docker
Create .env file similar to .env-example with your variables

`docker-compose up --build -d` 

Go to https://t.me/yourbotname

## Run without Docker

Setup Postgres and make changes in .env file
```python
DB_HOST=localhost
DB_PORT=5432
DB_NAME=yourdbname
DB_USER=yourdbuser
DB_PASS=yourdbpass
```
Run application

```python
python -m venv venv
venv/scripts/activate
pip install -r requirements.txt
alembic upgrade head
cd bot
py main.py
```
Go to https://t.me/yourbotname
 

## DB structure
### users
- tg_id: primary key. Telegram ID;
### conversations
- id: primary key. Conversation id;
- user_tg_id: foreign key to users.tg_id;
- user_message: string field. Contains user request;
- assistant_message: string field. Contains GigaChat assistant response;
