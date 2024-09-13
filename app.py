from flask import Flask, render_template, redirect, url_for, request
import random

app = Flask(__name__)

todos = [ #id, name and check status for each todo will be appended to this list
   
]

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def homepage():
   error_message = None
   if request.method == "POST":
      enter_task= request.form["enter-task"] #accesses the task they inputted, appends it to todos
      if not enter_task:
         error_message = "Task cannot be empty, try again."
      else:
         current_id = random.randint(1,1000) #unique id to access the task
         todos.append({
            "id": current_id,
            "name": enter_task,
            "checked": False, #default value of checked is false until user presses tickbox
            "completion-date": None,
            "show_date_form": False,
         })
         return redirect(url_for("homepage"))
   pending_tasks = [todo for todo in todos if not todo["checked"]] #puts todo in pending tasks if not checked
   completed_tasks = [todo for todo in todos if todo["checked"]] #opposite
   return render_template('index.html', pending_tasks=pending_tasks, completed_tasks=completed_tasks, error_message=error_message) #assigns todos to either pending or completed tasks, depending on whether they're checked

@app.route("/check/<int:todo_id>", methods= ["POST"])
def check_task(todo_id): #changes the check status of task
   for todo in todos:
      if todo["id"] == todo_id: #checks for match in id the user wants to check
         todo["checked"] = not todo["checked"]
         break
   return redirect(url_for("homepage"))


@app.route("/delete/<int:todo_id>", methods= ["POST"])
def delete_task(todo_id): #deletes task if it matches the id
   global todos
   for todo in todos:
      if todo["id"] == todo_id:
         todos.remove(todo)
   return redirect(url_for("homepage")) #redirects to mainpage



@app.route("/set_completion_date/<int:todo_id>", methods= ["POST"])
def set_completion_date(todo_id): 
   completion_date = request.form.get("completion_date")
   for todo in todos:
      if todo["id"] == todo_id: #checks for match in id the user wants to check
         todo["completion_date"] = completion_date
         break
   return redirect(url_for("homepage"))

if __name__ == "__main__":
   app.run(debug=True)

