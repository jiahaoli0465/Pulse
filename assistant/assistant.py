from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask import Flask, render_template, request, jsonify, session
import openai
import os
import json

assistantbot = Blueprint('assistantbot', __name__,
                        template_folder='templates')

# Initialize the OpenAI client
openai.api_key = os.environ.get("OPENAI_API_KEY")
client = openai.Client(api_key=openai.api_key)

# use an Assistant
assistant_id = 'asst_TPmdUIPcSwHxhMLGnHCY9Zdg'


def new_thread():
    if 'thread_id' not in session:
        thread = client.beta.threads.create()
        session['thread_id'] = thread.id
def reset_thread():
    new_thread = client.beta.threads.create()
    session['thread_id'] = new_thread.id
   
@assistantbot.route('/chatbot')
def show_home():
    # Start a new thread for each user session
    if 'thread_id' not in session:
        thread = client.beta.threads.create()
        session['thread_id'] = thread.id
    return render_template('/gpt/index.html')

@assistantbot.route('/chatbot/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    print(user_input)

    # Retrieve the thread ID from the user session
    thread_id = session.get('thread_id')

    # Add the user's message to the Thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    # Run the Assistant to process the conversation
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    # Wait for the Run to complete
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == 'completed':
            break

    # Retrieve the latest messages
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    # Find the index of the latest user message
    latest_user_msg_index = next(
        (i for i, m in enumerate(reversed(messages.data)) if m.role == 'user'),
        None
    )

    # Assuming messages are in chronological order, find the first assistant message after the latest user message
    reply = None
    if latest_user_msg_index is not None:
        for message in messages.data[-latest_user_msg_index:]:
            if message.role == 'assistant':
                reply = message.content[0].text.value
                break

    if reply is None:
        reply = "No response."
    return jsonify({"reply": reply})


if __name__ == '__main__':
    assistantbot.secret_key = os.urandom(24)
    assistantbot.run(debug=True)