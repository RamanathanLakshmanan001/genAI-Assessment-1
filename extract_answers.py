# websites:
# https://www.siemensgamesa.com
# https://www.us.hsbc.com
# https://slack.com
# https://zoom.us
# https://www.spotify.com
# https://us.pg.com
# https://www.pepsico.com
# https://www.airbus.com
# https://www.ge.com
# https://corporate.walmart.com



# Questions:
# "What is the company's mission statement or core values?",
# "What products or services does the company offer?",    
# "When was the company founded, and who were the founders?",
# "Where is the company's headquarters located?",
# "Who are the key executives or leadership team members?",
# "Has the company received any notable awards or recognitions?"


# API key : AIzaSyA6QOGBOILWAlhcT9buDEXr9p_hD5MORDA

import os
import time
import pandas as pd
from google import genai
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)


def query_gemini_api(model, context, question):
    """Send a query to the Gemini API and return the answer."""
    try:
        response = client.models.generate_content(
            model=model,
            contents=f"Context: {context}\n\nQuestion: {question}"
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error querying Gemini API: {e}")
        return "Error"
    
def get_answers_with_delay(model, context, questions, delay=2):
    """Generate answers for a list of questions with a delay between API calls."""
    answers = []
    for question in questions:
        answer = query_gemini_api(model, context, question)
        answers.append(answer)
        time.sleep(delay)
    return answers


def process_files_and_questions(model, csv_files, questions, output_file):
    """Process CSV files, ask questions using Gemini API, and save answers to a CSV file."""
    results = []
    
    for csv_file in csv_files:
        company_name = csv_file["company_name"]
        file_path = csv_file["file_path"]
        base_url = csv_file["base_url"]
        
        try:
            data = pd.read_csv(file_path)
            context = " ".join(data.astype(str).apply(lambda x: " ".join(x), axis=1))  # Combine all data as text
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            context = "Error reading file"
        

        answers = get_answers_with_delay(model, context, questions, delay=4)
        
        results.append([company_name, base_url, *answers])
    
    
    columns = ["Company Name", "Base URL"] + [questions[i] for i in range(len(questions))]
    results_df = pd.DataFrame(results, columns=columns)
    results_df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")


gemini_model = "gemini-2.0-flash" 

csv_files = [
    {"company_name": "siemensgamesa", "file_path": "./scraped_data_folder/website_1.csv", "base_url": "https://www.siemensgamesa.com"},
    {"company_name": "hsbc", "file_path": "./scraped_data_folder/website_2.csv", "base_url": "https://www.us.hsbc.com"},
    {"company_name": "slack", "file_path": "./scraped_data_folder/website_3.csv", "base_url": "https://slack.com"},
    {"company_name": "zoom", "file_path": "./scraped_data_folder/website_4.csv", "base_url": "https://zoom.us"},
    {"company_name": "spotify", "file_path": "./scraped_data_folder/website_5.csv", "base_url": "https://www.spotify.com"},
    {"company_name": "p&g", "file_path": "./scraped_data_folder/website_6.csv", "base_url": "https://us.pg.com"},
    {"company_name": "pepsico", "file_path": "./scraped_data_folder/website_7.csv", "base_url": "https://www.pepsico.com"},
    {"company_name": "airbus", "file_path": "./scraped_data_folder/website_8.csv", "base_url": "https://www.airbus.com"},
    {"company_name": "ge", "file_path": "./scraped_data_folder/website_9.csv", "base_url": "https://www.ge.com"},
    {"company_name": "walmart", "file_path": "./scraped_data_folder/website_10.csv", "base_url": "https://corporate.walmart.com"}
]

questions = [
    "What is the company's mission statement or core values?",
    "What products or services does the company offer?",
    "When was the company founded, and who were the founders?",
    "Where is the company's headquarters located?",
    "Who are the key executives or leadership team members?",
    "Has the company received any notable awards or recognitions?"
]

output_csv_file = "company_questions_answers.csv"

process_files_and_questions(gemini_model, csv_files, questions, output_csv_file)
