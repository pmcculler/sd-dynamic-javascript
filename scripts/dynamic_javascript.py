from asyncio.windows_events import NULL
import contextlib
import gradio as gr
import logging
from modules import scripts
from modules import script_callbacks

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import re

class JavascriptRunner:
    def __init__(self):
        options = Options()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def __del__(self):
        self.driver.quit()

    def execute_javascript_in_prompt(self, prompt, reset=False):
        sections = re.split('(%%.*?%%)', prompt, flags=re.DOTALL)
        for i, section in enumerate(sections):
        
            if section.startswith('%%') and section.endswith('%%'):
                # This is a JavaScript code section. Execute it.
                js_code = section[2:-2].strip()  # Remove the delimiters
                result = self.driver.execute_script(js_code)
                # Replace the JavaScript code with its output in the sections list
                replacement = str(result)
                if replacement != 'None' and replacement.__len__() > 0:
                    sections[i] = replacement
                else:
                    sections[i] = ""
        
        # Navigate to a blank page after executing JS
        # This 'resets' things like variables so they don't hang around between executions
        if reset:
            self.driver.get('about:blank')

        # Join the sections back together into the final output string
        prompt_out = ''.join(sections)
        return prompt_out


def _get_effective_prompt(prompts: list[str], prompt: str) -> str:
    return prompts[0] if prompts else prompt


class JSPromptScript(scripts.Script):
    def __init__(self) -> None:
        self.jr = NULL
        super().__init__()

    def title(self):
        return "Dynamic Javascript Prompt"

    def show(self, is_img2img):
        return scripts.AlwaysVisible
    
    def ui(self, is_img2img):
        is_enabled = gr.Checkbox(label="Enable Dynamic Javascript", value=True, elem_id=self.elem_id("enable"))
        return [is_enabled]

    def process(self, p, is_enabled):
        if not is_enabled:
            logging.debug("Dynamic javascript prompts disabled - exiting")
            return p

        # Save original prompts before we touch `p.prompt` etc.
        original_prompt = _get_effective_prompt(p.all_prompts, p.prompt)
        original_negative_prompt =_get_effective_prompt(
                p.all_negative_prompts,           
                p.negative_prompt,
            )
        
        all_prompts = p.all_prompts
        all_negative_prompts = p.all_negative_prompts

        try:
            if "%%" in original_prompt:
                if self.jr is NULL:
                    self.jr = JavascriptRunner();
                prompt_out = self.jr.execute_javascript_in_prompt(original_prompt)
                all_prompts = [prompt_out]
  
            if "%%" in original_negative_prompt:
                if self.jr is NULL:
                    self.jr = JavascriptRunner();
                # setting reset = true means after this the (variables) context is cleared.
                prompt_out = self.jr.execute_javascript_in_prompt(original_negative_prompt, True)
                all_negative_prompts = [prompt_out]

        except Exception as e:
            logging.exception(e)
            all_prompts = [str(e)]
            all_negative_prompts = [str(e)]

        p.all_prompts = all_prompts
        p.all_negative_prompts = all_negative_prompts
        p.prompt_for_display = original_prompt
        p.prompt = original_prompt
