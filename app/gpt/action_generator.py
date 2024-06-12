# app/openai/action_generator.py
from openai import Client
from app.config import settings

def generate_task_summary_and_action(message):
    
    # Set up OpenAI API
    # Initialize OpenAI client
    client = Client(api_key=settings.OPENAI_API_KEY)
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Your name is Gaia. You will help user to solve their problem.Act as a Hosting Specialist. You're working at Bukit Vista Company. Bukit Vista is a property management and rental services company in Bali, Indonesia. Your working time is 9 AM - 6 PM WITA (UTC+8). You are hospitable and helpful hosting specialist at Bukit Vista. You will help the company to welcoming guests and providing a pleasant experience from guest that confirmed their booking. You should help them pre-arrival, during stay, You will help the guest to solve their problem, guest request, and guest issues."},
            {"role": "user", "content": f"Message: {message}\n\nGenerate a task summary and actions required:"}
        ],
        model="gpt-3.5-turbo",
    )
    
    content = chat_completion.choices[0].message.content.strip()
    # Extract summary and action from content
    summary, action = content.split('\n\n', 1)
    return summary, action



if __name__ == "__main__":
    test_message = "Thank you, I left my used towels outside. Can I please have my bedsheets changed?"#"The light bulb in the bathroom is not working. Can you send someone to fix it?"
    summary, action = generate_task_summary_and_action(test_message)
    print("Summary:", summary)
    print("Action:", action)

