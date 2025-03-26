from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# Move model to GPU if available for faster inference
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generate_response(query: str, context: str, max_length: int = 100) -> str:
    """
    Generate a precise response to a query based on CSV context.
    
    Args:
        query (str): The user's question about the CSV data.
        context (str): Relevant CSV data as a string.
        max_length (int): Maximum length of the generated response.
    
    Returns:
        str: The model's answer to the query.
    """
    # Handle empty or invalid inputs
    if not query or not context:
        return "Error: Query or context is empty."

    # Craft a more instructive and structured prompt
    prompt = (
        "You are an expert assistant tasked with answering questions based on CSV data. "
        "Use the provided context to give a concise and accurate answer to the question. "
        "If the context doesn't contain enough information, say 'Insufficient data to answer.' "
        "Question: {query}\n"
        "Context (CSV data): {context}"
    ).format(query=query, context=context)

    try:
        # Tokenize the prompt and move to the appropriate device
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Generate response with optimized parameters
        outputs = model.generate(
            **inputs,
            max_length=max_length,  # Dynamic length based on query complexity
            num_beams=4,           # Beam search for better quality
            early_stopping=True,   # Stop when a good answer is found
            no_repeat_ngram_size=2 # Prevent repetitive phrases
        )

        # Decode and clean the response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        
        # Fallback for vague or empty responses
        if not response or len(response) < 3:
            return "Insufficient data to answer."
        
        return response

    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return f"Error: Unable to process the query due to {str(e)}"

# Example usage for testing
if __name__ == "__main__":
    # Sample query and context from your 'products.csv'
    sample_query = "What is the price of the Wireless Mouse?"
    sample_context = "Product ID: 1, Product Name: Wireless Mouse, Description: A high-precision wireless mouse with ergonomic design., Category: Electronics, Price: 29.99, Rating: 4.5, Stock: 100"
    
    response = generate_response(sample_query, sample_context)
    print(f"Query: {sample_query}")
    print(f"Context: {sample_context}")
    print(f"Response: {response}")