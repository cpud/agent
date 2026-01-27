import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    #print(f"Args: {args}")
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        #contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        #contents = args.user_prompt
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt,
                                           temperature=0,
                                           tools=[available_functions]),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response:")
        print(response.text)
    else:
        print(response.text)
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")


if __name__ == "__main__":
    main()
