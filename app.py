from flask import Flask, request, jsonify, render_template
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

pagination_template = """
<div class="pagination">
    <a href="?page={prev_page}">Prev</a>
    <a href="?page={next_page}">Next</a>
</div>
"""

def show_search_form():
    return search_template

def run_search(query, page=1, per_page=10):
    results = search(query)
    fi = Filter(results)
    filtered = fi.filter()
    rendered = search_template
    filtered["snippet"] = filtered["snippet"].apply(lambda x: html.escape(x))
    
    # Pagination
    start = (page - 1) * per_page
    end = start + per_page
    for index, row in filtered.iloc[start:end].iterrows():
        row['rank'] = start + index + 1  # update rank
        rendered += result_template.format(**row.to_dict())
    rendered += pagination_template.format(prev_page=max(1, page - 1), next_page=page + 1)
    return rendered

@app.route("/", methods=['GET', 'POST'])
def search_form():
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        query = request.form["query"]
        return run_search(query, page)
    else:
        return show_search_form()

@app.route("/relevant", methods=["POST"])
def mark_relevant():
    data = request.get_json()
    query = data["query"]
    link = data["link"]
    storage = DBStorage()
    storage.update_relevance(query, link, 10)
    return jsonify(success=True)

def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.run()