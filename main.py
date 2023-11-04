import customtkinter

from libs.simulationSettings.settings import Settings
from libs.ui.console import UI


def main():
    app = customtkinter.CTk()
    app.title("Obliczenia Ewolucyjne - Ackley")
    ui = UI(app)
    settings = Settings()
    # ui.test_graph()
    # ui.add_or_update_graph('Test',([1,2,3,4,5],[46,82,64,186,24]))
    # algorithmStart(-50, 50, 10, 10, 50, True, "integer", 2, 0.8, 0.3, 0.3, 30, "BEST", "ONE_POINT", "ONE_POINT", False)

    app.mainloop()


if __name__ == "__main__":
    main()
