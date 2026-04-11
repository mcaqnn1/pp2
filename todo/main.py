from fastapi import FastAPI, HTTPException
from models import Task
from schemas import TaskCreate, TaskUpdate

app = FastAPI()

tasks = []
task_id_counter = 1

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: TaskCreate):
    global task_id_counter
    new_task = Task(id=task_id_counter, title=task.title)
    tasks.append(new_task)
    task_id_counter += 1
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated: TaskUpdate):
    for task in tasks:
        if task.id == task_id:
            if updated.title is not None:
                task.title = updated.title
            if updated.completed is not None:
                task.completed = updated.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Task not found")