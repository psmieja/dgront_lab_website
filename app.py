from flask import Flask, render_template, url_for, send_from_directory 
import json

app = Flask(__name__)

def format_author_name(author_name_dict):
    formatted_name = f"{author_name_dict['surname']}, "
    for name in author_name_dict["firstname"].split():
        formatted_name += f"{name[0]}."
    return formatted_name

def author_list_to_string(author_list):
    if len(author_list) > 3:
        return f"{format_author_name(author_list[0])} et al."
    formatted_author_list = ""
    for author in author_list:
        formatted_author_list += f"{format_author_name(author)};"
    return formatted_author_list[:-1]

def prepare_articles(articles_file, only_featured=False):
        articles = json.load(articles_file)
        if only_featured:
            articles = [article for article in articles if article["featured"]]
        for article in articles: 
            article["authors"] = author_list_to_string(article["authors"])
        return articles


@app.route("/")
@app.route("/home")
def home():
    with open("./data/lab_members.json", "r") as lab_members_file, \
         open("./data/collaborators.json", "r") as collaborators_file, \
         open("./data/projects.json", "r") as projects_file, \
         open("./data/news.json", "r") as news_file, \
         open("./data/articles.json", "r") as articles_file:
        
        lab_members = json.load(lab_members_file)
        collaborators = json.load(collaborators_file)
        projects = json.load(projects_file)
        articles = prepare_articles(articles_file, only_featured=True)
        news = [news_item for news_item in json.load(news_file) if news_item["featured"]]
        
    return render_template('index.html',
                           lab_members=lab_members,
                           collaborators=collaborators,
                           projects=projects,
                           news=news,
                           articles=articles
                           )

@app.route("/publications")
def publications():
    with open("./data/articles.json", "r") as articles_file:
        articles = prepare_articles(articles_file)

    return render_template('publications.html',
                           articles=articles
                           )

@app.route("/uploads/<path:name>")
def download_file(name):
    return send_from_directory("uploads", name, as_attachment=True)

if __name__ == "__main__":
    app.run(port=8000, debug=True)