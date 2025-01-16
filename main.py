from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Example</title>
    </head>
    <body>
        <h1>Welcome to FastAPI</h1>
    </body>
    </html>
    """



app = FastAPI()

@app.get("/dynamic", response_class=HTMLResponse)
async def dynamic_template(request: Request):
    # Load and render the Mako template
    template = Template(filename="templates/example_templates.html")
    rendered_template = template.render(
        name="John Doe",
        current_time=datetime.now().strftime("%Y-%tm-%d %H:%M:%S")
    )
    return HTMLResponse(content=rendered_template)