from flaskcrud import app,db
from werkzeug.datastructures import RequestCacheControl
from flask import render_template, request, redirect
from .form import TodoForm
from bson import ObjectId

@app.route("/")
def view_page():
    Todos=[]
    for todo in db.todo_list.find():
        todo["_id"] = str(todo["_id"])
        Todos.append(todo)
    return render_template("view.html", todos=Todos)

@app.route("/addTodo", methods=["POST", "GET"])
def addTodo():
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name=form.name.data
        todo_description=form.description.data
        completed=form.completed.data

        db.todo_list.insert_one({
            "name": todo_name,
            "description": todo_description,
            "completed": completed
        })
        
        return redirect("/")
    else:
      form=TodoForm()
    return render_template("form.html", form=form)
@app.route("/delete/<id>")
def delete_todo(id):
    db.todo_list.find_one_and_delete({"_id": ObjectId(id)})
    return redirect("/")


@app.route("/update/<id>", methods = ['POST', 'GET'])
def update_todo(id):
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data

        db.todo_list.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
        }})
        return redirect("/")
    else:
        form = TodoForm()

        todo = db.todo_list.find_one_or_404({"_id": ObjectId(id)})
        print(todo)
        form.name.data = todo.get("name", None)
        form.description.data = todo.get("description", None)
        form.completed.data = todo.get("completed", None)

    return render_template("form.html", form = form)
