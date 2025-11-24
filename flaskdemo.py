import wikipedia
from flask import Flask, render_template, request, session, redirect, url_for


app = Flask(__name__)
# This Flask app sets app.secret_key, which is an encryption key used "to sign cookies and other things".
# Our app will work without it, but not completely. Without the secret key, we receive an error when searching:
# RuntimeError: The session is unavailable because no secret key was set.
# Storing secrets in plain code like this is not good practice. We know it.
# We don't want you to think we're endorsing this practice!
app.secret_key = 'IT@JCUA0Zr98j/3yXa R~XHH!jmN]LWX/,?RT'


@app.route('/')
def home():
    """Home page route."""
    return render_template("home.html")


@app.route('/about')
def about():
    """About page route."""
    return "I am still working on this"


@app.route('/search', methods=['POST', 'GET'])
def search():
    """Search page route. Return either form page to search, or search results."""
    if request.method == 'POST':
        session['search_term'] = request.form['search']
        return redirect(url_for('results'))
    return render_template("search.html")


@app.route('/results')
def results():
    """Results page route. Render the search results."""
    search_term = session['search_term']
    page = get_page(search_term)
    return render_template("results.html", page=page)


def get_page(search_term):
    """Get a Wikipedia page object based on the search term."""
    # This function is not a route
    try:
        page = wikipedia.page(search_term)
    except wikipedia.exceptions.PageError:
        # No such page, so return a random one
        page = wikipedia.page(wikipedia.random())
    except wikipedia.exceptions.DisambiguationError:
        # This is a disambiguation page; get the first real page (close enough)
        page_titles = wikipedia.search(search_term)
        # Sometimes the next page has the same name (different caps), so don't try the same again
        if page_titles[1].lower() == page_titles[0].lower():
            title = page_titles[2]
        else:
            title = page_titles[1]
        page = get_page(wikipedia.page(title))
    return page


if __name__ == '__main__':
    app.run()
