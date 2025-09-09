"""Module anglais_hello_world - affiche Hello World"""

# Nom lisible de l'exercice pour le menu principal
DISPLAY_NAME = "Anglais : Hello World"

from .utils import scroll_text
from .logger import log_result


def main() -> None:
    """Affiche le traditionnel message d'accueil."""

    scroll_text("hello world!\n")
    log_result("anglais_hello_world", 100)


if __name__ == "__main__":
    main()
