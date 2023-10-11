import openai
import tiktoken

def get_embedding(text: str, model: str = "text-embedding-ada-002"):
	text = text.replace("\n", " ")
	return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

def num_tokens(string: str, encoding_name: str = "cl100k_base") -> int:
	"""Returns the number of tokens in a text string."""
	encoding = tiktoken.get_encoding(encoding_name)
	token_count = len(encoding.encode(string))
	return token_count
 
def price_dollars(string: str, encoding_name: str = "cl100k_base") -> float:
	"""Returns the price of a text string in USD."""
	token_count = num_tokens(string, encoding_name)
	return (token_count / 1000) * 0.0004