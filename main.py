import inspect
import markdown
from datetime import datetime
import example_numpy  # TODO: remove hard-coded module import, utilize argparse

target_module = example_numpy  # TODO: remove hard-coded module import
start_time = datetime.now()

def format_docstring(docstring, indent, differentator):
    """
    Format an HTML docstring.

    Parameters
    ----------
    docstring : string
        The unformatted docstring.
    indent : int
        Number of pixels to add as indentation.
    differentator : string.
        The differentiator, e.g., "p" or "h2" or "summary".

    Returns
    -------
    string
        The formatted docstring.
    """
    lines = docstring.split(f"<{differentator}>")
    formatted_docstring = lines[0]
    lines = lines[1:]
    for line in lines:
        formatted_docstring += (
            f'<{differentator} style="margin-left: {indent}px;">{line}'
        )
    return formatted_docstring

def add_docstrings(f, object, indent):
    """
    Recursively find the docstrings of an object and its members,
     adding to an HTML script.
    
    Parameters
    ----------
    f : [file object](https://docs.python.org/3/glossary.html#term-file-object)
        The HTML file to which docstrings will be written.
    object : any
        An object with a docstring, i.e., `__doc__` attribute.
    indent : int
        Number of px for indentation in HTML paragraph.

    Returns
    -------
    None
    """
    time_difference = datetime.now() - start_time
    if time_difference.total_seconds() > 60:
        raise RuntimeError(
            "This program is taking too long."
        )
    indent += 10
    for name, obj in inspect.getmembers(object):
        if name.startswith("_") or name.startswith("__"):
            continue  # Ignore "private" types and functions
        if not (inspect.isfunction(obj) or inspect.isclass(obj)):
            continue  # We only care about classes and functions
        if obj.__doc__ is None:
            continue  # TODO: note classes and functions without docstrings, too
        try:
            html = markdown.markdown(obj.__doc__)
        except Exception:
            print(f"Couldn't convert docstring for {name}.")
            continue
        html = format_docstring(html, indent, "p")
        html = format_docstring(html, indent, "h2")
        f.write(
            f'<details><summary style="margin-left: {indent}px;">{name}</summary>'
        )
        f.write(html)  # Add docstring of obj
        add_docstrings(
            f, obj, indent
        )  # Recursively add members of obj before collapsing section
        f.write(("</details>"))
        # Close collapsible section of HTML script

def main():
    # Set up HTML script
    with open(f"{target_module.__name__}.html", "w") as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n")
        f.write(f"    <title>{target_module.__name__}</title>\n")
        f.write("</head>\n<body>\n")
        add_docstrings(
            f, target_module, 0
        )  # Recursively find members, add docstrings
        f.write("</body>\n</html>\n")


if __name__ == "__main__":
    main()
