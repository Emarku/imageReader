import openai

def open_ai_summary(input_data):
    '''This takes a prompt and returns openAI output'''

    # Set up your OpenAI API credentials
    openai.api_key = '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'

    # Define the chart data extracted from the image
    prompt_pre_amble = "interpret and summarize this data:"
    
    openai_prompt = str(prompt_pre_amble) + "\n"+ str(input_data)

    # Generate optimized text using ChatGPT API
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=openai_prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )

    optimized_text = response.choices[0].text.strip()

    return optimized_text
