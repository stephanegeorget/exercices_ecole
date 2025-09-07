"""Module anglais_hello_world - affiche Hello World"""

from .utils import scroll_text


def main() -> None:
    """Affiche le traditionnel message d'accueil."""

    scroll_text("hello world!\n")


if __name__ == "__main__":
    main()
