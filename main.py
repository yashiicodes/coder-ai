import os
import argparse
from dotenv import load_dotenv
from google import genai
from functions import get_file_content, get_files_info, run_python_file
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from google.genai import types
from prompts.prompts import system_prompt
from call_functions import available_functions, call_function


def get_input():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
# Now we can access `args.user_prompt`
    return args.user_prompt, args.verbose

def coder_ai():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt, verbose = get_input()

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    for _ in range(20):  # iteration limit

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=available_functions,
                system_instruction=system_prompt,
            ),
        )

        if verbose:
            print('User prompt: ' + user_prompt)
            print('Prompt tokens: ' + str(response.usage_metadata.prompt_token_count))
            print('Response tokens: ' + str(response.usage_metadata.candidates_token_count))

        #  Step 1: Add model responses to history
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        #  Step 2: If NO function calls → final answer → EXIT
        if not response.function_calls:
            if response.text:
                print("\nFinal response:\n")
                print(response.text)
            return

        #  Step 3: Execute function calls
        function_results = []

        for fc in response.function_calls:
            function_call_result = call_function(fc, verbose=verbose)

            # Validate
            if not function_call_result.parts:
                raise Exception("No parts returned from function call")

            part = function_call_result.parts[0]

            if not part.function_response:
                raise Exception("Missing function_response")

            tool_response = part.function_response.response

            if tool_response is None:
                raise Exception("Function response is None")

            function_results.append(part)

            if verbose:
                print(f"-> {tool_response}")

        # Step 4: Send tool results BACK to model
        messages.append(
            types.Content(role="user", parts=function_results)
        )

    # If loop finishes without final answer
    print("Error: Agent did not complete within 20 iterations.")

def main():
    print("Hello from coder-ai!")
    coder_ai()


if __name__ == "__main__":
    main()
