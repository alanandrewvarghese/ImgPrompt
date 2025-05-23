import streamlit as st
import json
import time

from aistudio import generate
from utils import format_prompt
from image_styles import style_categories, essential_styles


st.set_page_config(page_title="AI Image Prompt Generator", page_icon="🖼️", layout="wide")

if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []

# App header
st.markdown("# AI Image Prompt Generator ")
st.divider()

col1, col2, col3= st.columns([1, 4, 4])

with col1:
    st.subheader("Options")
    bg_color_enabled = False
    all_styles_enabled = False
    advanced_expander_enabled = False
    custom_styles_enabled = False
    generate_photorealistic_prompt = st.checkbox("Photorealistic", value=False)
    if not generate_photorealistic_prompt:
        bg_color_enabled = st.checkbox("Solid background", value=True)
        advanced_expander_enabled = st.checkbox("Advanced options", value=False)
        custom_styles_enabled = st.checkbox("Enable Styles", value=True)
        if custom_styles_enabled:
            all_styles_enabled = st.checkbox("Show All styles", value=False)
            
    models = [
        "gemini-2.5-flash-preview-05-20",
        "gemini-2.5-flash-preview-04-17",
        "gemini-2.5-pro-preview-05-06",
    ]
    
    gemini_models = st.expander("Models", expanded=True)
    with gemini_models:
        selected_model = st.selectbox(
            "Select a model",
            models,
            index=0,
            help="Choose the model for generating prompts",
        )

with col2:
    st.subheader("Image Generation")

    description = st.text_input(
        "What image would you like to generate?*",
        placeholder="e.g. A cat surfing on a wave at sunset",
        help="Describe the main subject and action of your image",
    )

    if custom_styles_enabled:
        style_options = [
            f"{category} - {style}"
            for category, styles in style_categories.items()
            for style in styles
        ]

        if all_styles_enabled:
            style = st.selectbox(
                "Choose a style", style_options, help="Select the visual style for your image"
            )
        else:
            style = st.selectbox(
                "Choose a style",
                essential_styles,
                help="Select the visual style for your image",
            )

        # Extract just the style name for later use
        selected_style = style.split(" - ")[-1]

    # Color options in an organized expander
    if bg_color_enabled:
        color_expander = st.expander("Color Settings")
        with color_expander:
            bg_color = st.color_picker("Background color", "#ffffff")

    # Advanced options in an expander
    if advanced_expander_enabled:
        advanced_expander = st.expander("Advanced Options")
        with advanced_expander:
            extra = st.text_area(
                "Additional details",
                placeholder="e.g. High resolution, dramatic lighting, 4K, ultra-detailed",
                help="Add technical specifications, mood, lighting details, etc.",
            )

            aspect_ratio = st.selectbox(
                "Aspect Ratio",
                ["Square (1:1)", "Portrait (3:4)", "Landscape (16:9)", "Cinematic (21:9)"],
            )

    # Generate button with visual emphasis
    generate_button = st.button(
        "✨ Generate Prompt", type="primary", use_container_width=True
    )

# Results display area
with col3:
    st.subheader("Results")

    if generate_button:
        if not description.strip():
            st.error("⚠️ Please enter an image description.")
        else:            
            if generate_photorealistic_prompt:
                prompt = f"create an ultra-realistic photograph of {description.strip()} taken with a Sony α7 III camera using an 85mm lens at an f/1.2 aperture. The image should be in 4K resolution, with a focus on capturing the intricate details of the subject. The lighting should be soft and natural, enhancing the textures and colors of the scene. The background should be blurred to create a bokeh effect, drawing attention to the main subject. The overall composition should evoke a sense of realism and depth, making the viewer feel as if they are part of the scene."
            else:
                prompt = f"Generate an image of {description.strip()}, styled as {selected_style}"
                
                if bg_color_enabled:
                    prompt += f", set against a solid {bg_color} background."
                else:
                    prompt += f"."

                if advanced_expander_enabled:
                    prompt += f" Aspect ratio: {aspect_ratio}."

                    if extra and extra.strip():
                        prompt += f" Extra requirements include: {extra.strip()}"

            with st.spinner("Generating your enhanced prompt..."):
                try:
                    system_instructions = """Act as a Prompt Enhancer AI that takes user-input prompts and transforms them into more engaging, detailed, and thought-provoking questions. Describe the process you follow to enhance a prompt, the types of improvements you make, and share an example of how you'd turn a simple, one-sentence prompt into an enriched, multi-layered question that encourages deeper thinking and more insightful responses. Output Format: {explanation: string, generated_prompt_for_generating_image: string}"""

                    response = json.loads(
                        generate(system_instructions=system_instructions, prompt=prompt, model=selected_model)
                    )
                    print("Response generated using:", selected_model)
                    generated_prompt = response.get(
                        "generated_prompt_for_generating_image", ""
                    )

                    if not generated_prompt:
                        st.error("Failed to generate a prompt. Please try again.")
                    else:
                        # Display input prompt
                        st.markdown("##### Input Prompt")
                        st.code(prompt, language="markdown")

                        # Display generated prompt with copy button
                        st.markdown("##### Enhanced Prompt")
                        formatted_prompt = format_prompt(generated_prompt)
                        st.code(formatted_prompt, language="markdown")
                            
                        # Save to history
                        st.session_state.prompt_history.append(
                            {
                                "prompt": formatted_prompt,
                                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            }
                        )

                except Exception as e:
                    st.error(f"Error generating prompt: {str(e)}")
    else:
        st.info(
            "Complete the form and click 'Generate Prompt' to create your AI image prompt"
        )

    # Show history of generated prompts
    if st.session_state.prompt_history:
        history_expander = st.expander("Prompt History")
        with history_expander:
            for i, item in enumerate(reversed(st.session_state.prompt_history)):
                st.markdown(
                    f"**{item['timestamp']}**"
                )
                if st.button(f"View #{i+1}", key=f"view_{i}"):
                    st.code(item["prompt"], language="markdown")
                    st.download_button(
                        label="📋 Save",
                        data=item["prompt"],
                        file_name=f"prompt_{item['timestamp'].replace(':', '-').replace(' ', '_')}.txt",
                        mime="text/plain",
                        key=f"save_{i}",
                    )
                st.divider()
