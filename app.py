import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


def get_db_connection():
    conn = sqlite3.connect('database.sqlite3')
    try:
        cur.execute("INSERT INTO posts (title, content, autor, lugar) VALUES (?, ?, ?, ?)",
            ('Primer Post', 'Contenido para el primer post', 'Francisco Aviña', 'Celaya')
            )

        cur.execute("INSERT INTO posts (title, content, autor, lugar) VALUES (?, ?, ?, ?)",
                    ('Segundo Post', 'Contenido para el segundo post', 'Francisco Aviña', 'Celaya')
                    )
        cur.execute("INSERT INTO posts (title, content, autor, lugar) VALUES (?, ?, ?, ?)",
                    ('Tercer Post', 'Contenido para el tercer post', 'Francisco Aviña', 'Celaya')
                    )
        conn.commit()
    except:
        print('Database already create')
    print('si se conecta')
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/')
@app.route('/index')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    newline = '\n'
    result = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    table_names = sorted(list(zip(*result))[0])
    print ("\n columnames for " + newline.join(table_names))
    for row in conn.execute('SELECT * FROM posts'): 
        print(row)
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        autor = request.form['autor']
        lugar = request.form['lugar']


        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO posts (title, content, autor, lugar) VALUES (?, ?, ?, ?)',
                         (title, content, autor, lugar))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        autor = request.form['autor']
        lugar = request.form['lugar']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?, autor= ?, lugar= ?'
                         ' WHERE id = ?',
                         (title, content, autor, lugar, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    print(post)
    flash('"{}" was successfully deleted!'.format(post[2]))
    return redirect(url_for('index'))


@app.route('/info')
def info():
	return render_template('info.html')

@app.route('/portafolio')
def portafolio():
	return render_template('portafolio.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

if __name__	 == '__main__':
	app.run(debug=True)