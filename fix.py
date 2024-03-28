from pynput.keyboard import Key, Controller
import time
import pyperclip
import ollama
from string import Template


controller = Controller()

PROMPT_TEMPLATE = Template(
    """Fix all typos and casing and punctuation in this text, but preserve all new line characters, and return only corrected text without any preamble:
    
    $text
    
    
    """
)

def fix_text(text, model):
    prompt = PROMPT_TEMPLATE.substitute(text=text)
    
    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response["message"]["content"]


def fix_current_line(model):

    controller.tap(Key.home)
    with controller.pressed(Key.shift):
        controller.tap(Key.end)

    time.sleep(0.1)
    fix_selection(model)


def fix_selection(model):

    # 1. Copy to clipboard
    with controller.pressed(Key.ctrl):
        controller.press("c")
        controller.release("c")

    # 2. Get text from clipboard
    time.sleep(0.1)
    text = pyperclip.paste()

    # 3. fix text
    fixed_text = fix_text(text, model)
    time.sleep(0.1)

    # 4. copy back to clipboard
    pyperclip.copy(fixed_text)
    time.sleep(0.1)

    # 5. Paste the text back
    with controller.pressed(Key.ctrl):
        controller.press("v")
        controller.release("v")