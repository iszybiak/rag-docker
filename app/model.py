import os
import traceback
import logging
from openai import OpenAI, OpenAIError

# Logger configuration
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# API Key downloading
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if API key is available
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key missing. Set OPENAI_API_KEY in .env.")

# OpenAI client initialization
client = OpenAI(api_key=OPENAI_API_KEY)

# Generating answer
def generate_answer(context, question):
    try:
        prompt = f"Using the information below, answer the question:\n\n{context}\n\nQuestion: {question}"
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        logger.error(f"Open API error: {e}")
        logger.error(traceback.format_exc())
        return ""
    except Exception as e:
        logger.error(f"Unexpected error while generating HTML: {e}")
        logger.error(traceback.format_exc())
        return ""