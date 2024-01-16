from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import Header, Footer, Static
from textual.containers import Grid, Container
from textual.color import Color
import numpy as np

class Cell(Static):

    def __init__(self, n=""):
        super().__init__()
        self.n = n
        self.styles.background = "lightblue"
        self.styles.content_align = ("center", "middle")

    def update(self, m):
        # if m == self.n:
        #     self.n = int(self.n)+m
        self.styles.background = Color(*np.random.randint(0, 255, 3))

    def render(self):
        return self.n

    def on_key(self, event):
        if event.key == "up":
            self.update(self.n)
        elif event.key == "down":
            self.update(self.n)
        elif event.key == "left":
            self.update(self.n)
        elif event.key == "right":
            self.update(self.n)


class GameApp(App):
    """A 2048 game using Textual"""
    TITLE = "2048"
    SUB_TITLE = "Play with directional arrows"

    CSS_PATH = "grid.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="n", action="newgame", description="New Game"),
    ]

    def __init__(self):
        super().__init__()
        self.cells = [Cell(str(0)) for _ in range(9)]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        yield Header()
        self.update_cells()
        for cell in self.cells:
           yield cell
        yield Footer()



    def update_cells(self):
        for cell in self.cells:
            cell.update(str(np.random.randint(1, 10)))

if __name__ == "__main__":
    app = GameApp()
    app.run()
