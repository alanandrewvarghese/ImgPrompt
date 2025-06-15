# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types

from dotenv import load_dotenv
load_dotenv()


def enhance_prompt_one(prompt="",response=""):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash-preview-05-20"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""{prompt}"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.1,
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["enhanced_prompt"],
            properties = {
                "process": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "enhanced_prompt": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(text="""I am a Prompt Enhancer AI. Your goal is to optimize user prompts into highly detailed and effective instructions for Gemini, especially for image generation.

Process:

I will pinpoint the main subject/objective.
I will add environmental, temporal, and situational details.
I will specify viewpoint, angle, or narrative perspective.
I will set artistic style, tone, or aesthetic.
I will include specific attributes, textures, and sensory information.
I will refine exclusions or priorities.
I will refine the image generation prompt to use only one option per element, no ORs, and make it as specific as possible.

Finally, I will present the user with the enhanced image generation prompt, formatted as a descriptive paragraph without using action-oriented words like 'create' or 'generate'."""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response = response + chunk.text
    return response