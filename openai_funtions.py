import openai
from sidebar import set_openai_api_key
def open_ai_summary(input_data,appKey):
    '''This takes a prompt and returns openAI output'''


    openai.api_key= appKey
    #openai.api_key = set_open_api_key(api_key_input)
    # Define the chart data extracted from the image
    prompt_pre_amble = "The following data has been extracted from a chart. Reinterpret the data in a clean form and give a shor summary and some insights:"
    
    openai_prompt = str(prompt_pre_amble) + "\n"+ str(input_data)

    # Generate optimized text using ChatGPT API
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=openai_prompt,
        max_tokens=100,
        n=1,
        temperature=0.7
    )

    optimized_text = response.choices[0].text.strip()

    return optimized_text
