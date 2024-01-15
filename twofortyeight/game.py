from textual.app import App, ComposeResult, RenderResult
from textual.binding import Binding
from textual.widgets import Header, Footer
from textual.containers import Container

class Game(Container):
    DEFAULT_CSS = """
        Game {
        width: 100%;
        border: solid white;
        padding-left: 3;
        padding-top: 1;
        padding-bottom: 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.game = self.create_game()
    
    def create_game(self):
        return "2048"

    def render(self) -> RenderResult:
        return self.game


class GameApp(App):
    """A 2048 game using Textual"""

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="n", action="newgame", description="New Game"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        yield Container(
            Header(),
            Game(),
            Footer(),
        )

    def on_mount(self) -> None:
        self.title = "2048"
        self.sub_title = "Play with directional arrows"


if __name__ == "__main__":
    app = GameApp()
    app.run()
