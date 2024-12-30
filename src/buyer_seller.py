from open_ai.open_ai import OpenAIAssistant
from dotenv import load_dotenv
from pprint import pprint
import os
import json

load_dotenv()

def process_classified_ad(text: str) -> dict:
    # Initialize with your API key
    api_key = os.getenv("OPENAI_API_KEY")
    assistant_manager = OpenAIAssistant(api_key)
    
    # Connect to your existing assistant
    assistant_id = os.getenv("BUYER_OR_SELLER_ASSISTANT_ID")
    assistant = assistant_manager.connect_to_assistant(assistant_id)
    
    # Create a thread and process the message
    thread = assistant_manager.create_thread()
    response = assistant_manager.process_message(text)
    
    # Parse and return the response as a dictionary
    return json.loads(response)

def main():
    # Example usage
    sample_text = """
        ქუთაისში იყიდება კორეული სახურავი 0.5მმ ახალი 3 ცალი 7.30 სმ იანები 22 კვ. მეტრი ასევე წყლის 4 ცალი ტრუბა, ერთ ნახევარი 4 მეტრიანი ღარი და 180 ცალი შურუფი! ფასი: კორეული ჟეშტი - 20 ლარი კვადრატი წყლის ტრუბები-80 ლარი ღარი-40 ლარი ტელ: 592016858 ან 598352864
    """
    result = process_classified_ad(sample_text)
    pprint(result)

if __name__ == "__main__":
    main()