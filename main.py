from fastapi import FastAPI, Request
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
async def create_task(request: Request):
    data = await request.json()
    title = data.get('title')
    if not title:
        return {'error': 'Title is required'}
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
async def get_tasks(request: Request):
    con = sqlite3.connect('kebula.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    con.close()
    return [{'id': task[0], 'title': task[1], 'completed': task[2]} for task in tasks]


@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    con = sqlite3.connect('kebula.db')
    cur = con.cursor()
    cur.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    con.commit()
    con.close()
    return {'message': 'Task deleted successfully'}
