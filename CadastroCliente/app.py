from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your-password',
    'database': 'cadastro_clientes_db'
}

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f'Error connecting to MySQL database {err}')
        raise



@app.route('/')
def index():
    conn = None
    cursor = None
    clients = []

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, nome, email, telefone, endereco FROM clientes ORDER BY nome ASC")
        clients = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Error fetching clients: {err}")
    except Exception as e:
        print(f"Unexpected error occurred while fetching clients: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return render_template('index.html', clients=clients)


@app.route('/add_client', methods=['POST'])
def add_client():
    if request.method == 'POST':
        nome = request.form.get('name')
        email = request.form.get('email')
        telefone = request.form.get('phone')
        endereco = request.form.get('address')

        conn = None
        cursor = None

        try:

            if not nome or not email:
                print("Error: Name and Email are required fields.")
                flash("Name and Email are required fields.", "warning")
                return redirect(url_for('index'))
            conn = get_db_connection()
            cursor = conn.cursor()

            sql = "INSERT INTO clientes (nome, email, telefone, endereco) VALUES (%s, %s, %s, %s)"
            val = (nome, email, telefone, endereco)

            cursor.execute(sql, val)
            conn.commit()

            print(f'Client {nome} has been added to database')
            flash(f'Client {nome} has been added to database', 'success')

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            if err.errno == 1062:
                print(f"Error: Email '{email}' already exists. {err}")
                flash(f"Email '{email}' already exists. {err}", 'danger')
            else:
                print(f"Error adding client: {err}")
                flash(f"Error adding client: {err}", 'danger')
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"An unexpected error occurred: {e}")
            flash(f"An unexpected error occurred: {e}", 'danger')

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/delete_client/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM clientes WHERE id = %s"
        val = (client_id,)

        cursor.execute(sql, val)
        conn.commit()

        print(f"Client with ID {client_id} has been deleted from database")
        flash(f'Client with ID {client_id} has been deleted from database', 'success')
    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        print(f"Database error deleting client with ID {client_id}: {err}")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"An unexpected python error occurred during deletion: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for('index'))



@app.route('/select_client_for_edit', methods=['POST'])
def select_client_for_edit():
    client_id = request.form.get('selected_client', type=int)
    if client_id is None:
        print("Error: No client selected for editing in select_client_for_edit.")
        flash("Please select a client to edit.", "warning")
        return redirect(url_for('index'))
    return redirect(url_for('edit_client', client_id=client_id))

@app.route('/edit_client/<int:client_id>', methods=['GET'])
def edit_client(client_id):
    conn = None
    cursor = None
    client = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT id, nome, email, telefone, endereco FROM clientes WHERE id = %s"
        val = (client_id,)

        cursor.execute(sql, val)
        client = cursor.fetchone()

        if client is None:
            print(f"Client with ID {client_id} not found for editing.")
            flash(f"Client with ID {client_id} not found for editing.", 'danger')
            return redirect(url_for('index'))

    except mysql.connector.Error as err:
        print(f"Database error editing client with ID {client_id}: {err}")
        return redirect(url_for('index'))
    except Exception as er:
        print(f"An unexpected error occurred fetching client for edit (ID {client_id}): {er}")

        return redirect(url_for('index'))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('edit_client.html', client=client)



@app.route('/update_client/<int:client_id>', methods=['POST'])
def update_client(client_id):
    if request.method == 'POST':
        nome = request.form.get('name')
        email = request.form.get('email')
        telefone = request.form.get('phone')
        endereco = request.form.get('address')

        # --- DEBUGGING ---
        print("\n--- Starting Client Update Debugging ---")
        print(f"Client ID received for update: {client_id}")
        print(f"New Nome: {nome}")
        print(f"New Email: {email}")
        print(f"New Telefone: {telefone}")
        print(f"New Endereco: {endereco}")


        conn = None
        cursor = None

        try:
            if not nome or not email:
                print("Error: Name and Email are required fields.")
                flash("Name and Email are required fields.", "warning")
                return redirect(url_for('edit_client', client_id=client_id))

            conn = get_db_connection()
            cursor = conn.cursor()

            sql = "UPDATE clientes SET nome = %s, email = %s, telefone = %s, endereco = %s WHERE id = %s"
            val = (nome, email, telefone, endereco, client_id)

            cursor.execute(sql, val)
            conn.commit()

            print(f"Client with ID {client_id} has been updated successfully.")
            flash(f"Client with ID {client_id} has been updated successfully.", 'success')

        except mysql.connector.Error as err:
            if conn:
               conn.rollback()
               print(f"MySQL Error during update for client ID {client_id}: {err}")
            if err.errno == 1062:
                flash(f"Error: Email '{email}' already exists for another client. Please use a different email.",
                      "danger")
            else:
                flash(f"Database error: {err}", "danger")
                return redirect(url_for('edit_client', client_id=client_id))
        except Exception as e:
            if conn:
                conn.rollback()
            print(f'An unexpected Python error occurred during updating client with ID {client_id}: {e}')
            flash(f"An unexpected error occurred: {e}", "danger")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return redirect(url_for('index'))

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
