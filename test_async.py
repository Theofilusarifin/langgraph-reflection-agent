from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
import asyncio

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
            "Always provide detailed recommendations, including requests for length, virality, style, etc.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
            " Generate the best twitter post possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


llm = ChatOpenAI()
generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm

# async def reflection():
#     print("reflection_start")
#     stream_generator = reflect_chain.astream({
#         "messages": [
#             {"role": "user", "content": "I think this world is trash"}
#         ]
#     })
#     async for chunk in stream_generator:
#         yield chunk.content
        

# async def generate():
#     print("generate_start")
#     stream_generator = generate_chain.astream({
#         "messages": [
#             {"role": "user", "content": "I think this world is trash"}
#         ]
#     })
#     async for chunk in stream_generator:
#         yield chunk.content
        
async def run_reflection():
    print("reflection_start")
    final_reflection = ""
    async for chunk in reflect_chain.astream({
        "messages":[{"role":"user","content":"I think this world is trash"}]
    }):
        final_reflection += chunk.content
        print("reflection: ", chunk.content)
    print("reflection_stop")
    return final_reflection
        

async def run_generate():
    print("generate_start")
    final_generate = ""
    async for chunk in generate_chain.astream({
        "messages":[{"role":"user","content":"I think this world is trash"}]
    }):
        final_generate += chunk.content
        print("generate: ", chunk.content)
    print("generate_stop")
    return final_generate


async def main():
    # 1) schedule them both immediately
    ref_task = asyncio.create_task(run_reflection())
    gen_task = asyncio.create_task(run_generate())

    # 2) wait for both to finish (they run concurrently)
    final_reflection, final_generate = await asyncio.gather(ref_task, gen_task)
    return final_reflection, final_generate
    
full_reflection, full_generate = asyncio.run(main())

print(full_reflection)