from os.path import isdir
from os import mkdir


class Html:

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
  <body>
  {self.build_folder(tree)}
  </body>
</html>
"""

    def build_folder(self, folder):
        return f"""<details>
        <h1>{folder['name'] if "name" in folder else ""}</h1>
        <section>
        {''.join([self.build_file(item) for item in folder['items']] if "items" in folder else "")}
        </section>
        </details>"""

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
