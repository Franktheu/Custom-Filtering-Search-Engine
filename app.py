from flask import Flask, request, jsonify, render_template
from flask import Flask, request, jsonify, render_template, url_for
from search import search
from filter import Filter
from storage import DBStorage
import html

app = Flask(__name__)

styles = """
<style>
    .site {
        font-size: .8rem;
        color: green;
    }
    
    .snippet {
        font-size: .9rem;
        color: gray;
        margin-bottom: 30px;
    }
    
    .rel-button {
        cursor: pointer;
        color: blue;
    }
</style>
<script>
const relevant = function(query, link){
    fetch("/relevant", {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
           "query": query,
           "link": link
          })
        });
}
</script>
"""

search_template = styles + """
    <div style="display: flex; justify-content: center; align-items: center; height: 9vh; background-color: white;">
        <form action="/" method="post" style="display: flex; border: 1px solid #ccc; border-radius: 24px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <input type="text" name="query" style="flex: 1; border: none; padding: 12px; font-size: 16px; outline: none; box-shadow: 0 0 5px lightblue;" placeholder="Enter query...">
            <input type="submit" value="Search" style="border: none; background-color: #4CAF50; color: white; font-size: 16px; padding: 12px 20px; cursor: pointer; border-radius: 0 24px 24px 0;">
        </form>
    </div>
"""
result_template = """
<p class="site">{rank}: {link} <span class="rel-button" onclick='relevant("{query}", "{link}");'>Relevant</span></p>
<a href="{link}">{title}</a>
<p class="snippet">{snippet}</p>
"""

def show_search_form():
    return search_template

def run_search(query, page=1):
    results = search(query, page)
    fi = Filter(results)
    filtered = fi.filter()
    rendered = search_template
    filtered["snippet"] = filtered["snippet"].apply(lambda x: html.escape(x))
    for index, row in filtered.iterrows():
        rendered += result_template.format(**row)
    
    if page > 1:
        rendered += '<a href="{}">Previous</a>'.format(url_for('search_form', query=query, page=page-1))
    rendered += '<a href="{}">Next</a>'.format(url_for('search_form', query=query, page=page+1))
    
    return rendered

@app.route("/", methods=['GET', 'POST'])
def search_form():
    print(f"Request method: {request.method}")
    if request.method == 'POST':
        query = request.form["query"]
    else:
        query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    print(f"Query: {query}, Page: {page}")
    if query:
        return run_search(query, page)
    else:
        return show_search_form()
        if query:
            return run_search(query, page)
        else:
            return show_search_form()
def mark_relevant():
    data = request.get_json()
    query = data["query"]
    link = data["link"]
    storage = DBStorage()
    storage.update_relevance(query, link, 10)
    return jsonify(success=True)