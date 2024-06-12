import json
from gpt.action_generator import generate_task_summary_and_action
from app.prep.endpoint import main_endpoint

def store_in_database(data):
    # Simulate storing in a cloud database
    print("Storing in database:", json.dumps(data, indent=2))

def run_simulation():
    data = main_endpoint()

    if data['classification'] == 'onsite':
        summary, action = generate_task_summary_and_action(data['message'])
        task_data = {
            'name': data['name'],
            'message': data['message'],
            'booking_id': data['booking_id'],
            'summary': summary,
            'action': action
        }
        store_in_database(task_data)
    else:
        print("Message classified as not onsite. No action required.")

if __name__ == "__main__":
    run_simulation()
