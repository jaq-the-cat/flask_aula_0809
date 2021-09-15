from application import widget

@widget.widget('submit')
def submit(content: str):
    return f'<button>{content}</button>'
