import os
import random
from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from enum import Enum
from pydantic import BaseModel
from typing import Tuple, List


class ModelProvider(str, Enum):
    """Enum for supported LLM providers"""

    ANTHROPIC = "Anthropic"
    DEEPSEEK = "DeepSeek"
    GEMINI = "Gemini"
    GROQ = "Groq"
    OPENAI = "OpenAI"
    OLLAMA = "Ollama"


class LLMModel(BaseModel):
    """Represents an LLM model configuration"""

    display_name: str
    model_name: str
    provider: ModelProvider

    def to_choice_tuple(self) -> Tuple[str, str, str]:
        """Convert to format needed for questionary choices"""
        return (self.display_name, self.model_name, self.provider.value)

    def has_json_mode(self) -> bool:
        """Check if the model supports JSON mode"""
        if self.is_deepseek() or self.is_gemini():
            return False
        # Only certain Ollama models support JSON mode
        if self.is_ollama():
            return "llama3" in self.model_name or "neural-chat" in self.model_name
        return True

    def is_deepseek(self) -> bool:
        """Check if the model is a DeepSeek model"""
        return self.model_name.startswith("deepseek")

    def is_gemini(self) -> bool:
        """Check if the model is a Gemini model"""
        return self.model_name.startswith("gemini")

    def is_ollama(self) -> bool:
        """Check if the model is an Ollama model"""
        return self.provider == ModelProvider.OLLAMA


# Define available models
AVAILABLE_MODELS = [
    LLMModel(display_name="[anthropic] claude-3.5-haiku", model_name="claude-3-5-haiku-latest", provider=ModelProvider.ANTHROPIC),
    LLMModel(display_name="[anthropic] claude-3.5-sonnet", model_name="claude-3-5-sonnet-latest", provider=ModelProvider.ANTHROPIC),
    LLMModel(display_name="[anthropic] claude-3.7-sonnet", model_name="claude-3-7-sonnet-latest", provider=ModelProvider.ANTHROPIC),
    LLMModel(display_name="[deepseek] deepseek-r1", model_name="deepseek-reasoner", provider=ModelProvider.DEEPSEEK),
    LLMModel(display_name="[deepseek] deepseek-v3", model_name="deepseek-chat", provider=ModelProvider.DEEPSEEK),
    LLMModel(display_name="[gemini] gemini-2.0-flash", model_name="gemini-2.0-flash", provider=ModelProvider.GEMINI),
    LLMModel(display_name="[gemini] gemini-2.5-flash", model_name="gemini-2.5-flash-preview-04-17", provider=ModelProvider.GEMINI),
    LLMModel(display_name="[gemini] gemini-2.5-pro", model_name="gemini-2.5-pro-exp-03-25", provider=ModelProvider.GEMINI),
    LLMModel(display_name="[groq] llama-4-scout-17b", model_name="meta-llama/llama-4-scout-17b-16e-instruct", provider=ModelProvider.GROQ),
    LLMModel(display_name="[groq] llama-4-maverick-17b", model_name="meta-llama/llama-4-maverick-17b-128e-instruct", provider=ModelProvider.GROQ),
    LLMModel(display_name="[openai] gpt-4.5", model_name="gpt-4.5-preview", provider=ModelProvider.OPENAI),
    LLMModel(display_name="[openai] gpt-4o", model_name="gpt-4o", provider=ModelProvider.OPENAI),
    LLMModel(display_name="[openai] o3", model_name="o3", provider=ModelProvider.OPENAI),
    LLMModel(display_name="[openai] o4-mini", model_name="o4-mini", provider=ModelProvider.OPENAI),
]

# Define Ollama models separately
OLLAMA_MODELS = [
    LLMModel(display_name="[google] gemma3 (4B)", model_name="gemma3:4b", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="[alibaba] qwen3 (4B)", model_name="qwen3:4b", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="[meta] llama3.1 (8B)", model_name="llama3.1:latest", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="[google] gemma3 (12B)", model_name="gemma3:12b", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="[mistral] mistral-small3.1 (24B)", model_name="mistral-small3.1", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="[google] gemma3 (27B)", model_name="gemma3:27b", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="[alibaba] qwen3 (30B-a3B)", model_name="qwen3:30b-a3b", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="[meta] llama-3.3 (70B)", model_name="llama3.3:70b-instruct-q4_0", provider=ModelProvider.OLLAMA),
]

# Create LLM_ORDER in the format expected by the UI
LLM_ORDER = [model.to_choice_tuple() for model in AVAILABLE_MODELS]

# Create Ollama LLM_ORDER separately
OLLAMA_LLM_ORDER = [model.to_choice_tuple() for model in OLLAMA_MODELS]


def get_model_info(model_name: str) -> LLMModel | None:
    """Get model information by model_name"""
    all_models = AVAILABLE_MODELS + OLLAMA_MODELS
    return next((model for model in all_models if model.model_name == model_name), None)


def get_random_api_key(api_key_env: str) -> str:
    """
    Get a random API key from a comma-separated list of API keys.
    
    Args:
        api_key_env: The environment variable name containing the API key(s)
    
    Returns:
        A randomly selected API key from the list
        
    Raises:
        ValueError: If no valid API keys are found
    """
    api_keys = os.getenv(api_key_env, "").split(",")
    api_keys = [key.strip() for key in api_keys if key.strip()]
    if not api_keys:
        raise ValueError(f"No API keys found in {api_key_env}")
    return random.choice(api_keys)


def get_model(model_name: str, model_provider: ModelProvider) -> ChatOpenAI | ChatGroq | ChatOllama | None:
    """
    Get an LLM model instance with proxy settings and random API key selection.
    
    Args:
        model_name: The name of the model to use
        model_provider: The provider of the model
        
    Returns:
        An instance of the appropriate LLM model
        
    Raises:
        ValueError: If required API keys are not found
    """


    if model_provider == ModelProvider.GROQ:
        api_key = get_random_api_key("GROQ_API_KEY")
        if not api_key:
            print(f"API Key Error: Please make sure GROQ_API_KEY is set in your .env file.")
            raise ValueError("Groq API key not found.  Please make sure GROQ_API_KEY is set in your .env file.")
        return ChatGroq(model=model_name, api_key=api_key)
    
    elif model_provider == ModelProvider.OPENAI:
        api_key = get_random_api_key("OPENAI_API_KEY")
        if not api_key:
            print(f"API Key Error: Please make sure OPENAI_API_KEY is set in your .env file.")
            raise ValueError("OpenAI API key not found.  Please make sure OPENAI_API_KEY is set in your .env file.")
        return ChatOpenAI(model=model_name, api_key=api_key)
    
    elif model_provider == ModelProvider.ANTHROPIC:
        api_key = get_random_api_key("ANTHROPIC_API_KEY")
        if not api_key:
            print(f"API Key Error: Please make sure ANTHROPIC_API_KEY is set in your .env file.")
            raise ValueError("Anthropic API key not found.  Please make sure ANTHROPIC_API_KEY is set in your .env file.")
        return ChatAnthropic(model=model_name, api_key=api_key)
    
    elif model_provider == ModelProvider.DEEPSEEK:
        api_key = get_random_api_key("DEEPSEEK_API_KEY")
        if not api_key:
            print(f"API Key Error: Please make sure DEEPSEEK_API_KEY is set in your .env file.")
            raise ValueError("DeepSeek API key not found.  Please make sure DEEPSEEK_API_KEY is set in your .env file.")
        return ChatDeepSeek(model=model_name, api_key=api_key)
    
    elif model_provider == ModelProvider.GEMINI:
        api_key = get_random_api_key("GOOGLE_API_KEY")
        # print("we use proxy")

        if not api_key:
            print(f"API Key Error: Please make sure GOOGLE_API_KEY is set in your .env file.")
            raise ValueError("Google API key not found.  Please make sure GOOGLE_API_KEY is set in your .env file.")
        # return ChatGoogleGenerativeAI(model=model_name, api_key=api_key)
        try:
            llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=api_key,
                    temperature=0.7,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=2048,
                    convert_system_message_to_human=True  # 添加这个参数
                )
            
            # try:
            #     test_response = llm.invoke("Hello")
            #     print("成功测试 Gemini 连接")
            # except Exception as e:
            #     print(f"测试 Gemini 连接时出错: {str(e)}")
            #     raise
            
            # logger.info(f"成功初始化 Gemini 模型: {model_name}")
            return llm
        except Exception as e:
            # logger.error(f"初始化 Gemini 模型时出错: {str(e)}")
                # 尝试使用备用配置
            try:
                llm = ChatGoogleGenerativeAI(
                        model=model_name,
                        google_api_key=api_key,
                        temperature=0.7,
                        convert_system_message_to_human=True
                )
                # logger.info(f"使用备用配置成功初始化 Gemini 模型: {model_name}")
                return llm
            except Exception as e2:
                # logger.error(f"使用备用配置初始化 Gemini 模型时出错: {str(e2)}")
                raise
    
    elif model_provider == ModelProvider.OLLAMA:
        # Ollama 不需要 API key，但需要代理设置
        ollama_host = os.getenv("OLLAMA_HOST", "localhost")
        base_url = os.getenv("OLLAMA_BASE_URL", f"http://{ollama_host}:11434")
        return ChatOllama(
            model=model_name,
            base_url=base_url
        )
