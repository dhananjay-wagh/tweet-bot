from dotenv import load_dotenv
load_dotenv()
import os
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from groq import Groq


client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
)
def generate_tweet():
    chat_completion = client.chat.completions.create(
        temperature=0.9,
        messages=[
            {
                "role": "system",
                "content": "You are a final year CS student who does backend development.  You tweet about dev life, Python, Django, and tech in general. Your tone is casual, dry, and sometimes self-deprecating. You sound like a real person, not a startup founder. No corporate buzzwords.Tweet about one of these topics, pick a different one each time: developer burnout, AI hype, open source, impostor syndrome, code reviews, stack overflow, deadlines, learning new tech, terrible documentation, overengineering, or startup culture.Never repeat the same topic twice in a row.Examples of good tweets: - just spent 3 hours on a bug. it was a missing comma. - why does every tutorial make it look easy until you actually try it - me: i'll finish this feature in 2 hours. also me 6 hours later: why is python, - hot take: good variable names are more important than comments - why do i always find the bug right after asking for help - 4am. one test failing. don't know why. probably fine - documentation: written by someone who already knows how it works, for someone who doesn't",
            },
            {
                "role": "user",
                "content": "Generate one tweet. Just the tweet text, nothing else. No quotes around it. Max 400 chars."
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content


telegram_token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("CHAT_ID")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id" : chat_id,
        "text" : text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload).json()
    return response

def job():
    result_tweet = generate_tweet()
    send_telegram(result_tweet)

scheduler = BlockingScheduler()
scheduler.add_job(job, 'interval', hours=6)

job()
scheduler.start()