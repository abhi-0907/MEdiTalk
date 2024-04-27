from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


template = """
    Your name is MediTalk, an expert medical assistant.You Answers Medical related questions only!!!
    Don't make up conversation and question.
    Just truthfully answer the {query}!!!
    """

prompt = PromptTemplate.from_template(template)



def load_llm():
    llm = LlamaCpp(model_path="B:\Quantization_LLM\quantized_model\mediTalk_Q4_1.gguf",
               temperature=0.3,
               max_tokens=300,
               callback_manager=callback_manager, verbose=True
)
    return llm



def query_meditalk(message):
    llm = load_llm()
    prompt_formatted_str: str = prompt.format(
    query=message)
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    #response = llm_chain.invoke(prompt_formatted_str)
    response = llm.invoke(prompt_formatted_str)
    return response


res = query_meditalk("I am having diarhea?")
print(res)