from models import Task
from storage import load_tasks, save_tasks
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


app = FastAPI(title="Focus Tree Web")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    tasks = load_tasks()
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})


@app.post("/add")
async def add_task(request: Request, title: str = Form(...)):
    tasks = load_tasks()

    # Генерируем ID для новой задачи
    if tasks:
        new_id = max(task.id for task in tasks) + 1
    else:
        new_id = 1

    new_task = Task(id=new_id, title=title, status="active")
    tasks.append(new_task)
    save_tasks(tasks)
    return RedirectResponse(url="/", status_code=303)


@app.post("/done/{task_id}")
async def mark_done(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.status = "completed"
            save_tasks(tasks)
            return RedirectResponse(url="/", status_code=303)
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/delete/{task_id}")
async def delete_task(task_id: int):
    tasks = load_tasks()
    task_to_delete = None
    for task in tasks:
        if task.id == task_id:
            task_to_delete = task
            break

    if task_to_delete:
        tasks.remove(task_to_delete)
        save_tasks(tasks)

    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
