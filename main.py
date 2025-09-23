import inspect
import markdown
from datetime import datetime
import example_numpy  # TODO: remove hard-coded module import, utilize argparse

target_module = example_numpy  # TODO: remove hard-coded module import
start_time = datetime.now()

def add_docstrings(f, object):
    """
    Recursively find the docstrings of an object and its members,
     adding to an HTML script.
    
    Parameters
    ----------
    f : [file object](https://docs.python.org/3/glossary.html#term-file-object)
        The HTML file to which docstrings will be written.
    object : any
        An object with a docstring, i.e., `__doc__` attribute.

    Returns
    -------
    None
    """
    time_difference = datetime.now() - start_time
    if time_difference.total_seconds() > 5:
        raise RuntimeError(
            "This program is taking too long."
        )
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
        f.write(f"<details><summary>{name}</summary>")
        f.write(html)  # Add docstring of obj
        add_docstrings(
            f, obj
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
            f, target_module
        )  # Recursively find members, add docstrings
        f.write("</body>\n</html>\n")


if __name__ == "__main__":
    main()
