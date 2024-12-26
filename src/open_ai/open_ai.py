import openai
import time
from typing import Dict, List, Optional

class OpenAIAssistant:
    def __init__(self, api_key: str):
        """
        Initialize OpenAI Assistant manager.
        
        Args:
            api_key (str): Your OpenAI API key
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.assistant = None
        self.thread = None
        self.current_run = None

    def create_assistant(
        self, 
        name: str,
        instructions: str,
        model: str = "gpt-4-turbo-preview",
        tools: Optional[List[Dict]] = None,
        file_ids: Optional[List[str]] = None
    ) -> Dict:
        """
        Create a new assistant with specified parameters.
        
        Args:
            name (str): Name of the assistant
            instructions (str): System instructions for the assistant
            model (str): Model to use (default: gpt-4-turbo-preview)
            tools (List[Dict], optional): List of tools to enable
            file_ids (List[str], optional): List of file IDs to attach
            
        Returns:
            Dict: Created assistant object
        """
        create_params = {
            "name": name,
            "instructions": instructions,
            "model": model,
        }
        
        if tools:
            create_params["tools"] = tools
        if file_ids:
            create_params["file_ids"] = file_ids

        self.assistant = self.client.beta.assistants.create(**create_params)
        return self.assistant

    def create_thread(self) -> Dict:
        """Create a new thread for conversation."""
        self.thread = self.client.beta.threads.create()
        return self.thread

    def add_message(self, content: str, role: str = "user") -> Dict:
        """
        Add a message to the current thread.
        
        Args:
            content (str): Message content
            role (str): Message role (default: "user")
            
        Returns:
            Dict: Created message object
        """
        if not self.thread:
            self.create_thread()
            
        return self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=role,
            content=content
        )

    def run_assistant(
        self, 
        instructions: Optional[str] = None,
        tools: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Run the assistant on the current thread.
        
        Args:
            instructions (str, optional): Additional instructions for this run
            tools (List[Dict], optional): Tools to use for this run
            
        Returns:
            Dict: Run object
        """
        run_params = {
            "assistant_id": self.assistant.id,
            "thread_id": self.thread.id,
        }
        
        if instructions:
            run_params["instructions"] = instructions
        if tools:
            run_params["tools"] = tools

        self.current_run = self.client.beta.threads.runs.create(**run_params)
        return self.current_run

    def wait_for_completion(self, interval: float = 1.0) -> Dict:
        """
        Wait for the current run to complete.
        
        Args:
            interval (float): Polling interval in seconds
            
        Returns:
            Dict: Completed run object
        """
        while True:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=self.current_run.id
            )
            
            if run.status in ["completed", "failed", "cancelled"]:
                self.current_run = run
                return run
                
            time.sleep(interval)

    def get_messages(self, limit: int = 20) -> List[Dict]:
        """
        Get messages from the current thread.
        
        Args:
            limit (int): Maximum number of messages to retrieve
            
        Returns:
            List[Dict]: List of message objects
        """
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id,
            limit=limit
        )
        return messages.data

    def get_last_response(self) -> Optional[str]:
        """
        Get the last assistant response from the thread.
        
        Returns:
            str: Last assistant message content, or None if no messages
        """
        messages = self.get_messages(limit=1)
        if messages and messages[0].role == "assistant":
            return messages[0].content[0].text.value
        return None

    def process_message(self, message: str) -> str:
        """
        Process a single message and return the assistant's response.
        
        Args:
            message (str): User message to process
            
        Returns:
            str: Assistant's response
        """
        self.add_message(message)
        self.run_assistant()
        self.wait_for_completion()
        return self.get_last_response()

    def upload_file(self, file_path: str) -> str:
        """
        Upload a file to use with the assistant.
        
        Args:
            file_path (str): Path to the file to upload
            
        Returns:
            str: File ID
        """
        with open(file_path, "rb") as file:
            response = self.client.files.create(
                file=file,
                purpose="assistants"
            )
        return response.id