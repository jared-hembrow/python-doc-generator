from os.path import isdir
from os import mkdir


class Html:
    style = """
    <style>
  body {
    font-family: sans-serif;
    margin: 0;
  }
  
  .container {
    margin: 20px;
  }
  
  details {
    margin: 1rem 0;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 1rem;
    background-color: #f8f8f8; /* Light gray background */
  }
  
  summary {
    cursor: pointer;
    font-weight: bold;
  }
  
  section {
    margin-left: 1rem;
  }
  
  .item {
    margin: 0.5rem 0;
    border: 1px solid #eee;
    border-radius: 3px;
    padding: 0.5rem;
    background-color: #f0f0f0; /* Lighter gray background */
  }
  
  .item h3 {
    margin-bottom: 0.25rem;
  }
  
  .doc-string-list-item {
    margin-left: 1rem;
    list-style-type: disc;
  }
  
</style>
    """

    def write_html_file(self, path):
        if not isdir(path):
            mkdir(path)
        with open(f"{path}/index.html", "w") as file:
            file.write(self.html)

    def build_html(self, tree):
        print(tree)
        self.html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Documentation</title>
  </head>
  {self.style}
  <body>
  <section class="container">
  {self.build_folder(tree)}
  </section>
  </body>
</html>
"""

    def build_folder(self, folder):
        print("\n\nFOLDER:", folder, "\n\n")
        return f"""<details>
        <summary>{folder['name'] if "name" in folder else ""}</summary>
        <section>
        {''.join([self.build_file(item) for item in folder['items']] if "items" in folder else "")}
        </section>
        </details>
        {''.join([self.build_folder(folder_item) for folder_item in folder['folders']]) if "folders" in folder else ""}
        """

    def build_file(self, file):
        if file["doc_strings"] is None:
            return ""
        print("File", file)
        start_tag = "<details>"
        title = f"<summary>{file['name']}</summary>"
        content = f"<p>{''.join([self.build_item(item) for item in file['doc_strings']['doc_strings']])}</p>"
        end_tag = "</details>"
        return start_tag + title + content + end_tag

    def build_item(self, item):
        print("ITEM", item)
        start_tag = '<article class="item">'
        title = f"<h3>{item['name']}</h3>"
        meta_items = self.build_meta_items(
            item["doc_strings"]["meta"] if item["doc_strings"] else ""
        )
        sub_items = (
            self.build_sub_item(item["sub_doc_strings"])
            if item["sub_doc_strings"]
            else ""
        )
        end_tag = "</article>"
        return start_tag + title + meta_items + sub_items + end_tag

    def build_sub_item(self, sub_item):
        print("ITEM", sub_item)
        sub_list = []
        for item in sub_item["doc_strings"]:
            sub_list.append(self.build_item(item))
        return "".join(sub_list)

    def build_meta_items(self, items):
        params = [item for item in items if item["args"][0] == "param"]
        returns = [item for item in items if item["args"][0] == "returns"]
        params_tag = f" {'<h3>Params</h3>' if len(params) > 0 else ''}{''.join([self.build_list_item(item) for item in params])}"
        returns_tag = f"{'<h3>Returns</h3>' if len(returns) > 0 else ''}{''.join([self.build_list_item(item) for item in returns])}"
        return params_tag + returns_tag

    def build_list_item(self, item):
        print("LIST ITEM", item)
        return f'<li class="doc-string-list-item">{item['arg_name'] if "arg_name" in item else ''} ({item['type_name']}){item['description']}</li>'
