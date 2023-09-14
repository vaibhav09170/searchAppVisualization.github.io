from flask import Flask, render_template, request
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Sample data (you should replace this with your own data)
data = {
    "Document 1": { "SP" :["1.SQL","2.SQL"], "JOBNAME" : ["job1"]},
    "Document 2": ["Document 4"],
    "Document 3": ["Document 5", "Document 6"],
    "Document 4": [],
    "Document 5": [],
    "Document 6": [],
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]
        results, tree = search(query)
        plot = create_tree_plot(tree)
        return render_template("index.html", results=results, plot=plot)
    return render_template("index.html")


def search(query):
    # In a real application, you would perform a search using an indexing system.
    # For simplicity, we'll just return documents that match the query.
    results = [doc for doc in data.keys() if query.lower() in doc.lower()]
    tree = create_search_tree(results)
    return results, tree


def create_search_tree(results):
    # Create a directed tree to represent the relationships between search results.
    tree = nx.DiGraph()
    for result in results:
        for related_result in data.get(result, []):
            tree.add_edge(result, related_result)
    return tree


def create_tree_plot(tree):
    pos = nx.spring_layout(tree)
    plt.figure(figsize=(8, 8))
    nx.draw(tree, pos, with_labels=True, node_size=5000, node_color="lightblue")
    plt.title("Search Results Tree")
    # Save the plot to a bytes object
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    # Encode the plot as base64 for rendering in HTML
    plot_data = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    return plot_data


if __name__ == "__main__":
    app.run(debug=True)
