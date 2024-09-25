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
def home():
    with open("./data/lab_members.json", "r") as f:
        lab_members = json.load(f)
    with open("./data/projects.json", "r") as f:
        projects = json.load(f)
    with open("./data/articles.json", "r") as f:
        articles = json.load(f)

    return render_template('index.html',
                           lab_members=lab_members,
                           projects=projects,
                           articles=articles
                           )


# if __name__ == '__main__':
    # app.run(debug=True)

if __name__ == "__main__":
    app.run(port=8000, debug=True)