from flask import Flask, render_template, url_for
import json
import base64

app = Flask(__name__)

# a workaround solution to avoid boilerplate code in templates
# a method is made available in jinja templates that provides paths to icons
# which are all placed in the same directory and are named consistently
# @app.context_processor
# def utility_processor():
#     def icon_path(tech):
#         return f"/static/icons/{tech}-icon.png"
#     return dict(icon_path=icon_path)


@app.route("/")
@app.route("/home")
def home():
    with open("./data/lab_members.json", "r") as lab_members_file, \
         open("./data/projects.json", "r") as projects_file, \
         open("./data/articles.json", "r") as articles_file:
        
        lab_members = json.load(lab_members_file)
        projects = json.load(projects_file)
        articles = json.load(articles_file)

    return render_template('index.html',
                           lab_members=lab_members,
                           projects=projects,
                           articles=articles
                           )

@app.route("/libra")
def libra():
    #  return redirect("http://www.example.com", code=302)
    return render_template('libra.html')




if __name__ == "__main__":
    app.run(port=8000, debug=True)

# if __name__ == '__main__':
    # app.run(debug=True)