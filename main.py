from fastapi import FastAPI, Request, HTTPException
import sqlite3

app = FastAPI()
con = sqlite3.connect('kebula.db')
cur = con.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
    id integer PRIMARY KEY autoincrement,
    title text not null,
    complite boolean default 0
    )
''')
con.commit()
con.close()


@app.post('/tasks')
async def create_task(request: Request, status_code=201):
    data = await request.json()
    title = data.get('title')
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    complite = data.get('complite', False)
    con = sqlite3.connect('kebula.db')
    cur = con.cursor()
    cur.execute('''
        INSERT INTO tasks (title, complite)
        VALUES (?, ?)
    ''', (title, complite))
    con.commit()
    task_id = cur.lastrowid
    con.close()
    return {'id': task_id, 'title': title, 'completed': complite}


@app.get('/tasks')
async def get_tasks(request: Request, status_code=200):
    con = sqlite3.connect('kebula.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    con.close()
    return [{'id': task[0], 'title': task[1], 'completed': task[2]} for task in tasks]


@app.get('/tasks/{task_id}')
async def get_task(task_id: int, status_code=200):
    con = sqlite3.connect('kebula.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cur.fetchone()
    con.close()
    if task:
        return {'id': task[0], 'title': task[1], 'completed': task[2]}
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@app.put('/tasks/{task_id}')
async def update_task(task_id: int, request: Request):
    data = await request.json()
    title = data.get('title')
    complite = data.get('complite')
    con = sqlite3.connect('kebula.db')
    cur = con.cursor()
    if title:
        cur.execute('UPDATE tasks SET title = ? WHERE id = ?', (title, task_id))
    if complite is not None:
        cur.execute('UPDATE tasks SET complite = ? WHERE id = ?', (complite, task_id))
    con.commit()
    con.close()
    return {'message': 'Task updated successfully'}


@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    con = sqlite3.connect('kebula.db')
    cur = con.cursor()
    cur.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    con.commit()
    con.close()
    return {'message': 'Task deleted successfully'}
