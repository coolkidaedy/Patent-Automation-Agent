import openai
from dotenv import load_dotenv
import os
# Load environment variables (make sure your .env contains OPENAI_API_KEY, etc.)
load_dotenv()

# Replace with your new OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Can you confirm if this works?"}
        ],
        max_tokens=1200,      
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Print out the response
    print("OpenAI Response:", response['choices'][0]['message']['content'])
except openai.error.AuthenticationError as e:
    print("Authentication Error: Check if your API key is correct.")
except openai.error.RateLimitError as e:
    print("Rate Limit Error: You may have exceeded your quota.")
except Exception as e:
    print(f"Unexpected Error: {e}")
