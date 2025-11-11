from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Главная страница (теперь проверяет, зарегистрирован ли пользователь)
@app.route('/')
def index():
    if session.get('username'):
        # Если пользователь зарегистрирован, показываем главную страницу
        return render_template('index.html', username=session['username'])
    else:
        # Если нет — перенаправляем на страницу регистрации
        return redirect(url_for('register'))

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Сохраняем данные в сессии
        session['username'] = username
        session['email'] = email

        # После регистрации перенаправляем на главную страницу
        return redirect(url_for('index'))

    return render_template('register.html')

# Страница ввода данных пользователя (например, BMR)
@app.route('/user_data', methods=['GET', 'POST'])
def user_data():
    if request.method == 'POST':
        age = request.form['age']
        weight = request.form['weight']
        height = request.form['height']
        activity_level = request.form['activity_level']

        session['age'] = age
        session['weight'] = weight
        session['height'] = height
        session['activity_level'] = activity_level

        return redirect(url_for('recommendations'))
    
    return render_template('user_data.html')

# Рекомендации (BMR и калории)
@app.route('/recommendations')
def recommendations():
    username = session.get('username')
    age = session.get('age')
    weight = session.get('weight')
    height = session.get('height')
    activity_level = session.get('activity_level')

    if not username:
        return redirect(url_for('register'))

    if activity_level == 'low':
        multiplier = 1.2
    elif activity_level == 'medium':
        multiplier = 1.55
    elif activity_level == 'high':
        multiplier = 1.9
    else:
        multiplier = 1.4

    if int(age) < 30:
        bmr = 15.3 * float(weight) + 679
    elif 30 <= int(age) < 60:
        bmr = 11.6 * float(weight) + 879
    else:
        bmr = 13.5 * float(weight) + 487

    calories_needed = bmr * multiplier

    return render_template('recommendations.html', username=username, calories_needed=calories_needed)

# Страница с советами и калькулятором
@app.route('/advice_and_calculator')
def advice_and_calculator():
    return render_template('advice_and_calculator.html')

# Страница рецептов
@app.route('/recipes')
def recipes():
    # Пример 50 рецептов
    recipes_list = []
    for i in range(1, 51):
        recipes_list.append({
            'name': f'Рецепт {i}',
            'calories_per_100g': 150,
            'ingredients': [f'Ингредиент {j}' for j in range(1, 4)],
            'instructions': f'Инструкция приготовления рецепта {i}'
        })
    return render_template('recipes.html', recipes=recipes_list)

# Избранные рецепты
@app.route('/favorites')
def favorites():
    favorite_recipes = session.get('favorites', [])
    return render_template('favorites.html', favorite_recipes=favorite_recipes)

@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    recipe_name = request.form['recipe_name']
    if 'favorites' not in session:
        session['favorites'] = []
    if recipe_name not in session['favorites']:
        session['favorites'].append(recipe_name)
    session.modified = True
    return redirect(url_for('favorites'))

@app.route('/remove_from_favorites', methods=['POST'])
def remove_from_favorites():
    recipe_name = request.form['recipe_name']
    if recipe_name in session.get('favorites', []):
        session['favorites'].remove(recipe_name)
    session.modified = True
    return redirect(url_for('favorites'))

# Выход
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('register'))

@app.route('/progress')
def progress():
    return render_template('progress.html')


if __name__ == '__main__':
    app.run(debug=True)
