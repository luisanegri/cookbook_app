from flask import Flask, render_template, redirect, request, url_for
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'cookbook_app'
app.config["MONGO_URI"] = 'mongodb://root:adminr00t@ds227481.mlab.com:27481/cookbook_app'
mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/breakfast')
def breakfast():
    return render_template("breakfast.html", recipes=mongo.db.recipes.find({"category_name": "Breakfast"}))


@app.route('/lunch')
def lunch():
    return render_template("lunch.html", recipes=mongo.db.recipes.find({"category_name": "Lunch"}))


@app.route('/snacks')
def snacks():
    return render_template("snacks.html", recipes=mongo.db.recipes.find({"category_name": "Snacks"}))


@app.route('/dinner')
def dinner():
    return render_template("dinner.html", recipes=mongo.db.recipes.find({"category_name": "Dinner"}))


@app.route("/all_recipes")
def all_recipes():
        return render_template(
                                'myrecipes.html',
                                recipes=mongo.db.recipes.find(),
                                categories=mongo.db.categories.find()
                              )


@app.route("/add_recipes")
def add_recipes():
    return render_template(
                            'addrecipes.html',
                            categories=mongo.db.categories.find(),
                            difficulty=mongo.db.difficulty.find()
                          )


@app.route("/insert_recipe", methods=['POST'])
def insert_recipe():
    # get recipes collection
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('all_recipes'))


@app.route("/read_recipe/<recipe_id>")
def read_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()
    return render_template('readrecipe.html', recipe=the_recipe, categories=all_categories)


@app.route("/edit_recipe/<recipe_id>", methods=['POST'])
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()
    all_dif_levels = mongo.db.difficulty.find()
    return render_template('editrecipe.html', recipe=the_recipe, categories=all_categories, difficulty=all_dif_levels)


@app.route("/update_recipe/<recipe_id>", methods=['POST'])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update(
        {"_id": ObjectId(recipe_id)},
        {
            "recipe_name": request.form.get['recipe_name'],
            "category_name": request.form.get['category_name'],
            "ingredients": request.form.get['ingredients'],
            "method": request.form.get['method'],
            "serves": request.form.get['serves'],
            "time_of_prep": request.form.get['time_of_prep'],
            "difficulty_level": request.form.get['difficulty_level']
        })
    return redirect(url_for('read_recipe'))


@app.route("/delete_recipe/<recipe_id>", methods=['POST'])
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    return redirect(url_for('all_recipes'))


if __name__ == '__main__':
        app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=False)
