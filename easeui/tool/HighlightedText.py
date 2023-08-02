import tkinter as tk
from pygments.lexers import PythonLexer

class HighlightedText(tk.Text):
    def __init__(self, *args, auto_tabs=False, **kwargs):
        super().__init__(*args, **kwargs)

        # Define tags for various token types
        self.tag_configure("Token.Keyword", foreground="orange")
        self.tag_configure("Token.Literal.String", foreground="green")
        self.tag_configure("Token.Operator", foreground="red")
        self.tag_configure("Token.Name", foreground="blue")

        # Set auto_tabs attribute
        self.auto_tabs = auto_tabs

        # Bind the Return key
        if auto_tabs:
            self.bind("<Return>", self.newline_and_indent)

    def highlight(self, event=None):
        # Remove all previous tags
        for tag in self.tag_names():
            self.tag_remove(tag, "1.0", "end")

        # Apply new tags
        last_col = 0
        last_line = 1
        data = self.get("1.0", "end-1c")
        for index, token, content in PythonLexer().get_tokens_unprocessed(data):
            lines = content.split("\n")
            if len(lines) > 1:  # the token contains new lines
                start_line = last_line
                start_col = last_col
                end_line = last_line = last_line + len(lines) - 1
                end_col = last_col = len(lines[-1])
            else:
                start_line = last_line
                start_col = last_col
                end_line = last_line
                end_col = last_col = last_col + len(content)
            self.tag_add(str(token), f"{start_line}.{start_col}", f"{end_line}.{end_col}")

    def newline_and_indent(self, event):
        # Insert a newline
        self.insert("insert", "\n")

        # Get the indentation of the previous line
        current_index = self.index("insert")
        last_line_index = str(int(current_index.split(".")[0]) - 1)
        last_line = self.get(f"{last_line_index}.0", "insert")
        indentation = len(last_line) - len(last_line.lstrip())

        # Increase indentation if the last line ends with a colon
        if last_line.strip().endswith(":"):
            indentation += 4

        # Insert the indentation
        self.insert("insert", " " * indentation)

        return "break"  # Prevent the default newline