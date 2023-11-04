import csv
import time
import tkinter as tk

import customtkinter
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from algorithm.algorithm import algorithmStart
from libs.patterns.singleton import Singleton
from libs.simulationSettings.settings import Settings
from .config import *

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")


class Graph:
    _id = None
    _root = None
    _ax = None
    _figure = None
    _title = ''
    _xlabel = ''
    _ylabel = ''
    _xs = np.array([])
    _ys = np.array([])
    _color = (np.random.random(), np.random.random(), np.random.random())
    _chart_type = None
    _annotation = None
    lines = []
    _hover = None

    def __init__(self, id, initial_data, root, labels=('', '')):
        self._id = id
        self._root = root
        self._figure = plt.Figure(figsize=(6, 5), dpi=100)
        self._ax = self._figure.add_subplot(111)
        x, y = initial_data
        self._xs = np.array([x])
        self._ys = np.array([y])
        self._ax.plot(self._xs, self._ys)
        self._chart_type = FigureCanvasTkAgg(self._figure, root)
        self._ax.set_title(id)
        self._xlabel, self._ylabel = labels
        self._title = id
        self._ax.set_xlabel(self._xlabel)
        self._ax.set_ylabel(self._ylabel)
        self._chart_type.get_tk_widget().pack()
        self._annotation = self._ax.annotate("", xy=(0, 0), xycoords='data', xytext=(15, 15),
                                             textcoords="offset points",
                                             bbox=dict(boxstyle="round", fc='white'),
                                             arrowprops=dict(arrowstyle="->"))
        self._annotation.set_visible(False)

    def update_data(self, data):
        # self._ax.clear()
        x, y = data
        self._xs = np.append(self._xs, [x])
        self._ys = np.append(self._ys, [y])

    def update_annot(self, line, idx):
        posx, posy = [line.get_xdata()[idx], line.get_ydata()[idx]]
        self._annotation.xy = (posx, posy)
        text = f'X: {posx:.2f} Y: {posy:.2f}'
        self._annotation.set_text(text)
        self._annotation.get_bbox_patch().set_alpha(0.4)

    def hover(self, event):
        vis = self._annotation.get_visible()
        if event.inaxes == self._ax:
            for line in self.lines:
                cont, ind = line.contains(event)
                if cont:
                    self.update_annot(line, ind['ind'][0])
                    self._annotation.set_visible(True)
                    self._figure.canvas.draw_idle()
                else:
                    if vis:
                        self._annotation.set_visible(False)
                        self._figure.canvas.draw_idle()

    def get_graph_id(self):
        return self._id

    def clear_graph_data(self):
        self._xs = np.array([])
        self._ys = np.array([])
        # clear graph
        self._ax.clear()
        # self._figure.canvas.delete('all')
        self._figure.canvas.mpl_disconnect(self._hover)
        for item in self._figure.canvas.get_tk_widget().find_all():
            self._figure.canvas.get_tk_widget().delete(item)
        self._chart_type.get_tk_widget().pack_forget()

    def draw(self, display, iterations):
        self._ax.set_title(self._title)
        self._ax.set_xlabel(self._xlabel)
        self._ax.set_ylabel(self._ylabel)
        colors = []
        self.lines = []
        for _ in range(iterations):
            colors.append((np.random.random(), np.random.random(), np.random.random()))
        for i in range(int(self._xs.size / iterations)):
            for j in range(iterations):
                start = j * int(self._xs.size / iterations)
                slicex = self._xs[start:i + start]
                slicey = self._ys[start:i + start]
                l, = self._ax.plot(slicex, slicey, c=colors[j])
                self.lines.append(l)
                self._figure.canvas.draw()
                display.update()
        self._hover = self._figure.canvas.mpl_connect("motion_notify_event", self.hover)


class UI(metaclass=Singleton):
    _menu = None
    _display = None
    _time = None
    _graphs = []
    allvars = []

    def _get_graph_by_id(self, id):
        for graph in self._graphs:
            if graph.get_graph_id() == id:
                return graph
        return None

    def add_or_update_graph(self, graph_id, data, labels=('', '')):
        graph = self._get_graph_by_id(graph_id)
        # epoch, _data = data
        # if isinstance(_data, np.ndarray):
        #     for i in range(_data.size):
        #         return self.add_or_update_graph(graph_id+str(i), (epoch, _data[i]),labels)
        if isinstance(graph, Graph):
            f = open(graph_id + ".csv", "a")
            writer = csv.writer(f)
            x, y = data
            writer.writerow([x, y])
            f.close()
            graph.update_data(data)
        else:
            f = open(graph_id + ".csv", "w")
            writer = csv.writer(f)
            labelx, labely = labels
            writer.writerow([labelx, labely])
            f.close()
            new_graph = Graph(graph_id, data, self._display)
            self._graphs.append(new_graph)
        self._display.update()

    def _handle_event(self, event, setter):
        if isinstance(event, str) and len(event) != 0:
            setter(event)
            return
        if len(event.widget.get()) != 0:
            setter(event.widget.get())

    def _dependencies_have_values(self, dependencies):
        for dependency in dependencies:
            if isinstance(dependency, str) and len(dependency) == 0:
                return False
            if len(dependency.get()) == 0:
                return False
        return True

    def __init__(self, root):
        # Window configuration
        root.geometry(WINDOW_SIZE)
        root.configure(bg=BACKGROUND_COLOR)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=8)
        root.grid_columnconfigure(1, weight=2)
        root.bind("<Button-1>", lambda event: event.widget.focus_set())
        algorithm_settings = Settings()

        # Define frames
        self._display = customtkinter.CTkScrollableFrame(root)
        self._menu = customtkinter.CTkScrollableFrame(root)

        self._display.grid(row=0, column=0, sticky="nsew", padx=(10, 10), pady=(20, 20))
        self._menu.grid(row=0, column=1, sticky="nsew", padx=(10, 10), pady=(20, 20))
        time_label_title = customtkinter.CTkLabel(self._display, text="Time: ")
        time_label_title.pack()
        self._time = tk.StringVar()
        time_label = customtkinter.CTkLabel(self._display, textvariable=self._time)
        time_label.pack()
        display_h1_label = customtkinter.CTkLabel(self._display, text="Grafy")
        display_h1_label.pack(pady=10)

        # MENU
        menu_h1_label = customtkinter.CTkLabel(self._menu, text="Menu")
        menu_h1_label.pack(pady=10)

        # Create input fields (Entry) with labels
        customtkinter.CTkLabel(self._menu, text="Amount of variables").pack()
        var_amt_var = tk.StringVar()
        var_amt_var.set(1)
        var_amt = customtkinter.CTkEntry(self._menu, textvariable=var_amt_var)
        var_amt.pack()

        customtkinter.CTkLabel(self._menu, text="Iteration count").pack()
        iter_amt_var = tk.StringVar()
        iter_amt_var.set(1)
        iter_amt = customtkinter.CTkEntry(self._menu, textvariable=iter_amt_var)
        iter_amt.pack()

        customtkinter.CTkLabel(self._menu, text="Beginning of the range - a").pack()
        menu_a_var = tk.StringVar()
        menu_a_var.set("-32.768")
        menu_a = customtkinter.CTkEntry(self._menu, textvariable=menu_a_var)
        menu_a.pack()

        customtkinter.CTkLabel(self._menu, text="End of the range - b").pack()
        menu_b_var = tk.StringVar()
        menu_b_var.set("32.768")
        menu_b = customtkinter.CTkEntry(self._menu, textvariable=menu_b_var)
        menu_b.pack()

        customtkinter.CTkLabel(self._menu, text="Population Amount").pack()
        menu_population_var = tk.StringVar()
        menu_population_var.set(100)
        menu_population_amount = customtkinter.CTkEntry(self._menu, textvariable=menu_population_var)
        menu_population_amount.pack()

        customtkinter.CTkLabel(self._menu, text="Precision").pack()
        menu_precision_var = tk.StringVar()
        menu_precision_var.set(5)
        menu_num_precision = customtkinter.CTkEntry(self._menu, textvariable=menu_precision_var)
        menu_num_precision.pack()

        customtkinter.CTkLabel(self._menu, text="Epochs amount").pack()
        menu_epochs_var = tk.StringVar()
        menu_epochs_var.set(300)
        menu_epochs_amount = customtkinter.CTkEntry(self._menu, textvariable=menu_epochs_var)
        menu_epochs_amount.pack()
        menu_epochs_amount.bind("<FocusOut>", lambda event: self._handle_event(event, algorithm_settings.set_epochs))

        customtkinter.CTkLabel(self._menu, text="Elite Stategy amount").pack()
        menu_elite_strategy_var = tk.StringVar()
        menu_elite_strategy_var.set(1)
        menu_elite_strategy_amount = customtkinter.CTkEntry(self._menu, textvariable=menu_elite_strategy_var)
        menu_elite_strategy_amount.pack()

        customtkinter.CTkLabel(self._menu, text="Cross Probability").pack()
        menu_cross_prob_var = tk.StringVar()
        menu_cross_prob_var.set(0.8)
        menu_cross_probability = customtkinter.CTkEntry(self._menu, textvariable=menu_cross_prob_var)
        menu_cross_probability.pack()

        customtkinter.CTkLabel(self._menu, text="Mutation probability").pack()
        menu_mutation_prob_var = tk.StringVar()
        menu_mutation_prob_var.set(0.3)
        menu_mutation_probability = customtkinter.CTkEntry(self._menu, textvariable=menu_mutation_prob_var)
        menu_mutation_probability.pack()

        customtkinter.CTkLabel(self._menu, text="Inversion probability").pack()
        menu_inversion_prob_var = tk.StringVar()
        menu_inversion_prob_var.set(0.2)
        menu_inversion_probability = customtkinter.CTkEntry(self._menu, textvariable=menu_inversion_prob_var)
        menu_inversion_probability.pack()

        customtkinter.CTkLabel(self._menu, text="Best amount/amount of tournaments").pack()
        menu_best_tournament_var = tk.StringVar()
        menu_best_tournament_var.set(10)
        menu_best_tournament_amount = customtkinter.CTkEntry(self._menu, textvariable=menu_best_tournament_var)
        menu_best_tournament_amount.pack()

        check_var = tk.StringVar()
        check_var.set("on")
        checkbox = customtkinter.CTkCheckBox(self._menu, text="Binary", variable=check_var, onvalue="on",
                                             offvalue="off")
        checkbox.pack(padx=20, pady=10)

        customtkinter.CTkLabel(self._menu, text="Choose Selection method").pack()
        selection_methods = ["BEST", "ROULETTE", "TOURNAMENT"]
        menu_selection_var = tk.StringVar()
        menu_selection_var.set("BEST")  # Default value
        menu_selection_method = customtkinter.CTkOptionMenu(self._menu, values=selection_methods,
                                                            variable=menu_selection_var)
        menu_selection_method.pack()

        customtkinter.CTkLabel(self._menu, text="Choose cross method").pack()
        cross_methods = ["ONE_POINT [B]", "TWO_POINTS [B]", "THREE_POINTS [B]", "UNIFORM [B]", "ARITHMETIC [D]",
                         "AVERAGE [D]", "BLEND_AB [D]", "BLEND_A [D]", "FLAT [D]", "HEURISTIC [D]"]
        menu_cross_var = tk.StringVar()
        menu_cross_var.set("ONE_POINT [B]")  # Default value
        menu_cross_method = customtkinter.CTkOptionMenu(self._menu, values=cross_methods, variable=menu_cross_var)
        menu_cross_method.pack()

        customtkinter.CTkLabel(self._menu, text="Choose mutation method").pack()
        mutation_methods = ["ONE_POINT [B]", "TWO_POINTS [B]", "BOUNDARY [B]", "UNIFORM [D]", "INDEX [D]", "GAUSS [D]"]
        menu_mutation_var = tk.StringVar()
        menu_mutation_var.set("ONE_POINT [B]")  # Default value
        menu_mutation_method = customtkinter.CTkOptionMenu(self._menu, values=mutation_methods,
                                                           variable=menu_mutation_var)
        menu_mutation_method.pack()

        customtkinter.CTkLabel(self._menu, text="Maximization").pack()
        maximization_methods = ["True", "False"]
        menu_maximization_var = tk.StringVar()
        menu_maximization_var.set("False")  # Default value
        menu_maximization_method = customtkinter.CTkOptionMenu(self._menu, values=maximization_methods,
                                                               variable=menu_maximization_var)
        menu_maximization_method.pack()

        self.allvars = [menu_a_var, menu_b_var, menu_population_var, menu_precision_var, menu_epochs_var,
                        menu_elite_strategy_var, menu_cross_prob_var, menu_mutation_prob_var,
                        menu_inversion_prob_var, menu_best_tournament_var, menu_selection_var, menu_cross_var,
                        menu_mutation_var,
                        menu_maximization_var, var_amt_var, iter_amt_var, check_var]
        customtkinter.CTkLabel(self._menu, text="").pack()

        start_button = customtkinter.CTkButton(self._menu, text="Start", command=self.start_algorithm_button)
        start_button.pack()

    def start_algorithm_button(self):
        s = Settings()
        s.set_range(self.allvars[0].get(), self.allvars[1].get())
        s.set_variable_amount(int(self.allvars[14].get()))
        s.set_population(self.allvars[2].get())
        s.set_precision(self.allvars[3].get())
        s.set_epochs(self.allvars[4].get())
        s.set_elite_settings(self.allvars[5].get())
        s.cross_settings.set_probability(self.allvars[6].get())
        s.mutation_settings.set_probability(self.allvars[7].get())
        s.inversion_settings.set_probability(self.allvars[8].get())
        s.set_best_chromosomes_tournament_group_size(self.allvars[9].get())
        s.set_selection_type(self.allvars[10].get())
        s.cross_settings.set_method(self.allvars[11].get())
        s.mutation_settings.set_method(self.allvars[12].get())
        s.set_is_maximum(self.allvars[13].get())
        range = s.get_range()
        a = range["start"]
        b = range["end"]
        var_amount = s.get_variable_amount()

        for graph in self._graphs:
            graph.clear_graph_data()
            del graph
        self._graphs = []

        init_time = time.time()

        isDecimal = False if self.allvars[16].get() == 'on' else True

        bestX, bestY = algorithmStart(
            var_amount, int(self.allvars[15].get()), a, b, s.get_population(), s.get_precision(),
            s.get_epochs(), s.get_elite_strategy_integer(),
            s.cross_settings.get_probability(), s.mutation_settings.get_probability(),
            s.inversion_settings.get_probability(),
            s.get_chromosomes(), s.get_selection_type(), s.cross_settings.get_method(),
            s.mutation_settings.get_method(), s.get_is_maximum(), isDecimal, self
        )

        totalTime = time.time() - init_time
        timePerIteration = totalTime / int(self.allvars[15].get())

        self._time.set(f"{totalTime}s total, {timePerIteration}s per iteration \n \n "
                       f"Best X = {bestX}, Best Y = {bestY}")

        for graph in self._graphs:
            graph.draw(self._display, int(self.allvars[15].get()))
