# app/bedrock_client_deepseek.py
from app.aws_client import create_bedrock_client
from botocore.exceptions import ClientError

class BedrockClientDeepseek:
    """Client for interacting with AWS Bedrock using the Deepseek-R1 model."""
    
    def __init__(self, config):
        """Initialize the Deepseek client with configuration."""
        self.model_id = config["model_id"]
        # Use the universal boto3 client for AWS Bedrock
        self.bedrock_runtime = create_bedrock_client(config)
    
    def create_conversation(self, user_message, system_message="You're a helpful assistant"):
        """Create conversation structure with system and user messages."""
        system_messages = [{"text": system_message}]
        messages = [{
            "role": "user",
            "content": [{"text": user_message}]
        }]
        return {
            "system_messages": system_messages,
            "messages": messages
        }
    
    def query_model(self, conversation_data, max_tokens=8192, temperature=0.5, top_p=0.9):
        """Non-streaming query to the Deepseek model."""
        try:
            response = self.bedrock_runtime.converse(
                modelId=self.model_id,
                messages=conversation_data["messages"],
                system=conversation_data["system_messages"],
                inferenceConfig={
                    "maxTokens": max_tokens, 
                    "temperature": temperature, 
                    "topP": top_p
                },
            )
            
            response_text = response["output"]["message"]["content"][0]["text"]
            reason_response = response["output"]["message"]["content"][1]["reasoningContent"]['reasoningText']['text']
            
            return {
                "response_text": response_text,
                "reasoning_text": reason_response
            }
            
        except (ClientError, Exception) as e:
            raise Exception(f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}")
    
    def stream_query_model(self, conversation_data, max_tokens=8192, temperature=0.5, top_p=0.9):
        """
        Stream both the final response and the reasoning tokens.
        
        Iterates over events from the streaming API and yields a dictionary indicating 
        whether the token belongs to the final response or the reasoning.
        """
        try:
            response = self.bedrock_runtime.converse_stream(
                modelId=self.model_id,
                messages=conversation_data["messages"],
                system=conversation_data["system_messages"],
                inferenceConfig={
                    "maxTokens": max_tokens, 
                    "temperature": temperature, 
                    "topP": top_p
                },
            )
            
            stream = response.get("stream")
            if not stream:
                raise Exception("No stream in response")
            
            for event in stream:
                if "contentBlockDelta" in event:
                    delta = event["contentBlockDelta"]["delta"]
                    # Distinguish between reasoning and final text
                    if "reasoningContent" in delta:
                        yield {"part": "reasoning", "text": delta["reasoningContent"]["text"]}
                    elif "text" in delta:
                        yield {"part": "final", "text": delta["text"]}
                        
        except (ClientError, Exception) as e:
            raise Exception(f"ERROR: Can't stream conversation for '{self.model_id}'. Reason: {e}")
