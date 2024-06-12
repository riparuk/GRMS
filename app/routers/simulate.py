from fastapi import APIRouter
from pydantic import BaseModel
from app.gpt.action_generator import generate_task_summary_and_action
import random
import string
from app.prep.preprocessing import classify_message

router = APIRouter()

class TaskData(BaseModel):
    name: str
    message: str
    booking_id: int
    classification: str

def generate_dummy_data():
    names = ['John Doe', 'Jane Smith', 'Alice Johnson']
    messages = [
        'Thank you, I left my used towels outside. Can I please have my bedsheets changed?',
        'The light bulb in the bathroom is not working. Can you send someone to fix it?',
        'Can I get an extra pillow and blanket?',
        'what the price for the room?',
        "my room’s door is broken, help me! ",
        "My room is very dirty, please clean it.",
        "The air conditioner in the villa is not working, can someone come and fix it?",
        "There's a leak in the bathroom, can you send maintenance?",
        "The lights in the hallway are flickering, could you send someone to check it?",
        "hello"
    ]
    booking_ids = [''.join(random.choices(
        string.ascii_uppercase, k=10)) for _ in range(3)]

    return random.choice(names), random.choice(messages), random.choice(booking_ids)

@router.post("/simulate/")
async def simulate():
    name, message, booking_id = generate_dummy_data()
    classification = classify_message(message)

    if classification == 'onsite':
        summary, action = generate_task_summary_and_action(message)
        task_data = {
            'name': name,
            'message': message,
            'booking_id': booking_id,
            'summary': summary,
            'action': action
        }
        # Simulate storing in a cloud database
        print("Storing in database:", task_data)
    else:
        print("Message classified as not onsite. No action required.")

    return task_data
