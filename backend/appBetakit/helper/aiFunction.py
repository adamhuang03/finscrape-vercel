import os
import requests
from openai import OpenAI # poetry add openai
from dotenv import load_dotenv # poetry add python-dotenv
from pprint import pprint
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env.local')
load_dotenv(dotenv_path)

instr_core = """
        You are an expert in finance and you understand the capital markets well. You have 10
        years of experience in the field, and your strength lie in understand articles or 
        content you read.
        """

class SystemInstructionError(Exception):
    pass

class AccessGPT:

    headers: str
    client: OpenAI
    system: str

    def __init__(self) -> None:
        self.headers = headers
        self.system = None
        self.client = OpenAI(
            organization=os.environ.get('ORGANIZATION_ID'),
            # project=os.environ.get('OPENAI_API_KEY') -- Only relevant for specific projects, pass in the Key as part of the header
        )

    def list_models(self):
        """Returns a list of openai.types.model.Model objects.

        See structure of these objects here: https://platform.openai.com/docs/api-reference/models/list

        For each item, you can call:
        1. id: name of the model
        2. object: type of object
        3. created: creation id
        4. owned_by: who owns it

        """
        model_list = list(self.client.models.list())
        return model_list
    
    def set_system_instruction(self, instruction: str):
        self.system = instruction

    def complete(self, inp: str) -> dict[str, str]:
        """Returns a ChatCompletionMessage.

        content: your response from the LLM
        function_call
        tool_calls
        """
        if not self.system:
            raise SystemInstructionError('No instructions have been given.')
        completion = self.client.chat.completions.create( # self._post under the hood, can assume it is a CRUD web server API request
            # model="gpt-3.5-turbo-0125",
            model='gpt-4o',
            messages=[
                {"role": "system", "content": self.system},
                {"role": "user", "content": inp}
            ]
        )
        return completion.choices[0].message

    def summary_analysis_inp(self, combo_text, word):
        inp = f"""
        You will be given a combined text of title and description. These are quick blurbs
        from a webpage that has alot of finance articles. You will also be given a word/phrase in
        which you will see if the combined text of title and description is relevant. If the
        word/phrase mentions a numerical constraint, make sure to capture that in the relevancy score. 

        Word/phrase: {word}
        
        Combined text of a title and description:
        {combo_text}

        If the above is relevant, you will give a number '1', If it is not relevant, you will give
        a number '0'.
        """

        return inp
    
    def content_analysis_inp(self, combo_text, word, content):
        inp = f"""
        Word/phrase: {word}
        
        Combined text of a title and description:
        {combo_text}

        Content from article:
        {content}

        ------------------------

        Above, you are given three things:
        1) a word/phrase
        2) combined text of title and description
        3) content from article

        Using the content from article and combined title/description, create a 
        summary of the events based on the contraint of the given word/phrase.
        The summary should be concise in one to two sentences only. The summary
        should encapsulate parties involved in the events, money that is used or
        transacted (if there is not money, it is undisclosed), and other important
        details.

        NOTE: Numerical constraints (ie. greater than 10 million) must be abided
        diligently! 
        NOTE: Indicate currency of value inside the article!
        NOTE: Keep standard formatting, no headers, just body text

        Sample:
        Boeing is investing $240 million CAD into Québec’s new aerospace innovation zone as part of a broader $415 million CAD project that includes additional financial commitments from companies like Bombardier and Airbus, aiming to strengthen the local aerospace industry through initiatives focused on decarbonization and advanced technology development.

        I will tip you $1,000 if you do a good job!
        """

        return inp


if __name__ == '__main__':
    main = AccessGPT()
    main.set_system_instruction(instruction=instr_core)
    text_test_1 = """
        Amii secures $3 million from PrairiesCan to fuel AI adoption in the Prairies; 
        Alberta AI hub aims to give SMBs tools and knowledge to leverage AI.
        """
    text_test_2 = """
        'Xanadu’s Christian Weedbrook is raising another $200 million to build a quantum data centre; 
        The CEO of Canada’s quantum unicorn is very optimistic about the country’s innovation potential.'
        """
    inp = main.summary_analysis_inp(
        combo_text=text_test_2,
        word='invest'
    )
    result = main.complete(inp=inp)
    print(result.content)
    
    