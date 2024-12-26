from open_ai.open_ai import OpenAIAssistant
from dotenv import load_dotenv
import os

load_dotenv()

# Example usage
def main():
    # Initialize with your API key
    api_key = os.getenv("OPENAI_API_KEY")
    assistant_manager = OpenAIAssistant(api_key)
    
    # Create an assistant
    assistant = assistant_manager.create_assistant(
        name="Georgian Word Form Generator",
        instructions="""You are an expert in Georgian language.
        When given a Georgian word, generate all its grammatical forms.
        For example, if the word is "სახლი" (house), return:
            სახლი
            სახლმა
            სახლს
            სახლის
            სახლით
            სახლად

        Give me in JSON format.
        """,



        model="gpt-4-turbo-preview"
    )
    
    # Create a thread
    thread = assistant_manager.create_thread()
    
    # Example conversation
    response = assistant_manager.process_message("Generate forms for the word 'თიფოქსი'")
    print("Assistant response:", response)
    
    # Or use it in a conversation loop
    while True:
        user_input = input("Enter a word (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
            
        response = assistant_manager.process_message(user_input)
        print("Assistant:", response)

if __name__ == "__main__":
    main()