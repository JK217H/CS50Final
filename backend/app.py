# app.py
import sqlite3
from flask import Flask
from flask_cors import CORS
from flask import jsonify
from flask import request
app = Flask(__name__)
CORS(app)  # Allow requests from your Vue frontend

def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/project-tag', methods =['POST'])
def add_tag():
    if request.method == 'OPTIONS':
        return '', 204
    datap = request.get_json()
    conn = None
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('INSERT INTO project_tags (tag) VALUES(?)', (datap.get('tag'),))
        tag_id = c.lastrowid  # ← Get the new ID
        conn.commit()
        conn.close()
        return jsonify({'id': tag_id})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Tag already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()
@app.route('/project-tags')
def get_project_tags():
    conn = get_db_connection()
    ptags = conn.execute('SELECT * FROM project_tags ORDER BY id DESC').fetchall()
    conn.close()
    ptags_list = [dict(row) for row in ptags]
    return jsonify(ptags_list)

@app.route('/project-tags/ptag/<id>')
def get_project_specific_tasks(id):
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE tag = ? ORDER BY id DESC', (id,)).fetchall()
    conn.close()
    tasks_list = [dict(row) for row in tasks]
    return jsonify(tasks_list)

@app.route('/task', methods=['POST'])
def add_task():
    if request.method == 'OPTIONS':
        return '', 204
    data = request.get_json()
    conn = None
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('INSERT INTO tasks (title, description, date, tag, status) VALUES (?, ?, ?, ?,?)', (data.get('title'), data.get('description'),data.get('date'), data.get('tag'), data.get('status')))
        task_id = c.lastrowid  # ← Get the new ID
        conn.commit()
        return jsonify({'id': task_id}) 
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Sqlite error'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()
 # ← Send it back as JSON

@app.route('/tasks')
def get_tasks_active():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE status ="active" ORDER BY id DESC').fetchall()
    conn.close()
    tasks_list = [dict(row) for row in tasks]
    return jsonify(tasks_list)
    
@app.route('/tasks/closed')
def get_tasks_closed():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE status ="closed" ORDER BY id DESC').fetchall()
    conn.close()
    tasks_list = [dict(row) for row in tasks]
    return jsonify(tasks_list)
@app.route('/tasks/date/active/<date>')
def get_tasks_by_date_active(date):
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE date = ? AND status="active" ORDER BY id DESC', (date,)).fetchall()
    conn.close()
    tasks_list = [dict(row) for row in tasks]
    return jsonify(tasks_list)
@app.route('/tasks/date/closed/<date>')
def get_tasks_by_date_closed(date):
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE date = ? AND status="closed" ORDER BY id DESC', (date,)).fetchall()
    conn.close()
    tasks_list = [dict(row) for row in tasks]
    return jsonify(tasks_list)

@app.route('/tasks/tag/<tag>')
def get_tasks_by_tag(tag):
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE tag = ?', (tag,)).fetchall()
    conn.close()
    tasks_list = [dict(row) for row in tasks]
    return jsonify(tasks_list)
@app.route('/tasks/task/<int:id>/status', methods=['PATCH'])
def update_task_status(id):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET status = CASE WHEN status ="active" THEN "closed" ELSE "active" END WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Status toggled successfully'})

@app.route('/calendar-tasks')
def get_calendar_tasks():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE date is NOT NULL ORDER BY date').fetchall()
    conn.close()
    tasks_list = [dict(row) for row in tasks]
    return jsonify(tasks_list)
@app.route('/tasks/<int:id>', methods=['GET'])
def get_single_task(id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    conn.close()
    if task:
        return jsonify(dict(task))
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:id>', methods=['PATCH'])
def update_task(id):
    data = request.get_json()
    conn = get_db_connection()
    try:
        conn.execute('UPDATE tasks SET title = ?, description = ?, date = ?, tag = ?, status = ? WHERE id = ?',
                     (data.get('title'), data.get('description'), data.get('date'),
                      data.get('tag'), data.get('status'), id))
        conn.commit()
        return jsonify({'message': 'Task updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    try:
        # Remove tag from project_tags table
        conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
        conn.commit()
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()



@app.route('/project-tags/<old_tag>', methods=['PATCH'])
def rename_project_tag(old_tag):
    data = request.get_json()
    new_tag = data.get('new_tag')

    if not new_tag:
        return jsonify({'error': 'New tag name is required'}), 400

    conn = get_db_connection()
    try:
        # Update tag name in project_tags table
        conn.execute('UPDATE project_tags SET tag = ? WHERE tag = ?', (new_tag, old_tag))

        # Update tag in all related tasks
        conn.execute('UPDATE tasks SET tag = ? WHERE tag = ?', (new_tag, old_tag))

        conn.commit()
        return jsonify({'message': 'Tag renamed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
@app.route('/project-tags/<tag>', methods=['DELETE'])
def delete_project_tag(tag):
    conn = get_db_connection()
    try:
        # Remove tag from project_tags table
        conn.execute('DELETE FROM project_tags WHERE tag = ?', (tag,))

        # Set tag to empty string in tasks
        conn.execute('UPDATE tasks SET tag = "" WHERE tag = ?', (tag,))

        conn.commit()
        return jsonify({'message': 'Tag deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)

