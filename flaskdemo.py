import wikipedia
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
# 这个密钥随便写，只要是个字符串就行，用来支持 session
app.secret_key = "ITQJCUA0Zr98j/3yXa R~XHH!jmN]LWX/,?RT"


@app.route("/")
def home():
    """Home page route."""
    return render_template("home.html")


@app.route("/about")
def about():
    """About page route."""
    return render_template("about.html")




@app.route("/search", methods=["GET", "POST"])
def search():
    """Search page route. Shows form (GET) or saves term then redirects (POST)."""
    if request.method == "POST":
        search_term = request.form["search"]
        session["search_term"] = search_term
        return redirect(url_for("results"))
    return render_template("search.html")


@app.route("/results")
def results():
    """Results page route. Show the page title and summary for the search term."""
    search_term = session.get("search_term", "")
    if not search_term:
        # 没有搜索词就回到搜索页
        return redirect(url_for("search"))

    page = get_page(search_term)
    return render_template("results.html", page=page, search_term=search_term)


def get_page(search_term: str):
    """Get a Wikipedia page object based on the search term."""
    try:
        # 正常情况：直接用搜索词取页面
        page = wikipedia.page(search_term)
    except wikipedia.exceptions.PageError:
        # 没有这个页面，就随机给一个
        page = wikipedia.page(wikipedia.random())
    except wikipedia.exceptions.DisambiguationError:
        # 歧义页面，试着选一个更像的结果
        page_titles = wikipedia.search(search_term)
        if len(page_titles) > 2 and page_titles[1].lower() == page_titles[0].lower():
            title = page_titles[2]
        elif len(page_titles) > 1:
            title = page_titles[1]
        else:
            title = search_term
        page = wikipedia.page(title)
    return page


if __name__ == "__main__":
    app.run()
