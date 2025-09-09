"""Petit exercice d'histoire"""

# Nom lisible de l'exercice pour le menu principal
DISPLAY_NAME = "Histoire : La préhistoire"

from .utils import scroll_text
from .logger import log_result


def main() -> None:
    """Affiche une phrase d'histoire."""

    scroll_text("La préhistoire c'est ce qu'il y a avant l'histoire.\n")
    log_result("hist_test", 100)
