from flask import Flask, request, jsonify
import mysql.connector
import hashlib

app = Flask(__name__)

mydb = mysql.connector.connect(
  host="localhost",
  user="Leader",
  password="nJ_aqk8901!nJ_aqk8901!",  
  database="users"
)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        cursor = mydb.cursor(prepared=True) 
        query = "SELECT password FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            hashed_password = result[0]
            if hash_password(password) == hashed_password:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False, "message": "Неверный пароль"})
        else:
            return jsonify({"success": False, "message": "Пользователь не найден"})
    except mysql.connector.Error as err:
        return jsonify({"success": False, "message": f"Ошибка базы данных: {err}"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка: {e}"})

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        hashed_password = hash_password(password)

        cursor = mydb.cursor(prepared=True) 
        query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        cursor.execute(query, (email, hashed_password))
        mydb.commit()
        return jsonify({"success": True})
    except mysql.connector.Error as err:
        if err.errno == 1062: 
            return jsonify({"success": False, "message": "Email уже занят"})
        else:
            return jsonify({"success": False, "message": f"Ошибка при регистрации: {err}"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка: {e}"})

if __name__ == '__main__':
    app.run(debug=True)
