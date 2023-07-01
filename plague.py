import os
from matplotlib import pyplot as plt
from matplotlib import ticker

# class object to simulate infecting the World
class Plague(object):

    def __init__(self):

        self.infected_percentage_curve_ = [0.] # percentage of the sick population
        self.infection_rate_curve_ = [0.]   # percentage / day
        self.infection_control_curve_ = [0.]    # percentage / day

    def _infectionDisappearanceRate(self):

        p = self.infected_percentage_curve_[-1]

        return .5 * p * p

    # method to apply the control
    def spreadPlague(self, infection_control):
        """
    applies the control signal to spread the plague and updates the status curves

    Arguments:
    ----------

    infection_control: float, infection rate to be added to the current infection rate

        """

        # update infection rate according to control signal
        curr_infection_rate = self.infection_rate_curve_[-1]
        infection_rate = max(0., min(.6, curr_infection_rate + infection_control))

        effective_infection_rate = infection_rate - self._infectionDisappearanceRate()

        # update the infected percentage after 0.1 Day of infection with the current rate
        infection_percentage = \
            min(1., self.infected_percentage_curve_[-1] + effective_infection_rate * .1)

        # update status curves
        self.infected_percentage_curve_.append(infection_percentage)
        self.infection_rate_curve_.append(infection_rate)
        self.infection_control_curve_.append(infection_control)

    # method to obtain measurements
    def checkInfectionStatus(self):
        """
    returns the current infected percentage and infection rate as a two-tuple
    (infected_percentage, infection_rate)

    Returns:
    ----------

    (infected_percentage, effective_infection_rate): (float, float) tuple,
                    infection percentage and rate to be used by the controller

        """

        infected_percentage = self.infected_percentage_curve_[-1]
        effective_infection_rate = \
            self.infection_rate_curve_[-1] - self._infectionDisappearanceRate()

        return (infected_percentage, effective_infection_rate)

    # method to visualize the results for the homework
    def viewPlague(self, point_ss, plague_cost, save_dir='', filename='plague', show_plot=True):
        """
        plots multiple curves for the plague and
            saves the resultant plot as a png image

        Arguments:
        ----------

        point_ss: int, the estimated iteration index at which the system is at steady state

        plague_cost: float, the estimated cost of the infection until the steady state

        save_dir: string, indicating the path to directory where the plot image is to be saved

        filename: string, indicating the name of the image file. Note that .png will be automatically
        appended to the filename.

        show_plot: bool, whether the figure is to be shown

        Example:
        --------

        visualizing the results of the infection

        # assume many control signals have been consecutively applied to spread the plague

        >>> my_plague = Plague()

        >>> my_plague.spreadPlague(infection_control) # assume this has been repeated many times

        >>> # assume state state index and the plague spread cost have been computed

        >>> # as point_ss=k and plague_cost=c

        >>> my_plague.viewPlague(point_ss=k, plague_cost=c,
        >>>                      save_dir='some\location\to\save', filename='plague')

        """

        color_list = ['#ff0000', '#32CD32', '#0000ff', '#d2691e', '#ff00ff', '#000000', '#373788']
        style_list = ['-', '--']

        num_plots = 3

        plot_curve_args = [{'c': color_list[k],
                            'linestyle': style_list[0],
                            'linewidth': 3} for k in range(num_plots)]

        plot_vert_args = [{'c': color_list[k],
                            'linestyle': style_list[1],
                            'linewidth': 3} for k in range(num_plots)]

        font_size = 18

        fig, axes = plt.subplots(3, 1, figsize=(16, 12))

        day_x = [i * .1 for i in range(len(self.infected_percentage_curve_))]
        x_ticks = day_x[::10]

        # infected population
        ax = axes[0]
        ax.set_title('infected population percentage over days', loc='left', fontsize=font_size)
        ax.plot(day_x[:point_ss+1], self.infected_percentage_curve_[:point_ss+1], **plot_curve_args[0])
        ax.plot(day_x[point_ss:], self.infected_percentage_curve_[point_ss:], **plot_curve_args[1])
        ax.plot([day_x[point_ss]] * 2, [0, self.infected_percentage_curve_[point_ss]], **plot_vert_args[2])


        ax.set_xlabel(xlabel='day', fontsize=font_size)
        ax.set_ylabel(ylabel='infected population %', fontsize=font_size)
        ax.set_xticks(x_ticks)
        ax.xaxis.set_minor_locator(ticker.FixedLocator([day_x[point_ss]]))
        ax.xaxis.set_minor_formatter(ticker.ScalarFormatter())
        ax.tick_params(which='minor', length=17, color='b', labelsize=13)
        ax.tick_params(labelsize=15)
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)
        ax.grid(True, lw = 1, ls = '--', c = '.75')

        # infection rate
        ax = axes[1]
        ax.set_title('infection rate over days', loc='left', fontsize=font_size)
        ax.plot(day_x[:point_ss + 1], self.infection_rate_curve_[:point_ss + 1],
                **plot_curve_args[0])
        ax.plot(day_x[point_ss:], self.infection_rate_curve_[point_ss:],
                **plot_curve_args[1])
        ax.plot([day_x[point_ss]] * 2, [0, self.infection_rate_curve_[point_ss]],
                **plot_vert_args[2])
        ax.fill_between(day_x[:point_ss + 1], 0, self.infection_rate_curve_[:point_ss + 1],
                        facecolor='#FF69B4', alpha=0.7)

        ax.text(1.5, .01, 'cost = %.2f'%plague_cost,
                horizontalalignment='center', fontsize=font_size)

        ax.set_xlabel(xlabel='day', fontsize=font_size)
        ax.set_ylabel(ylabel='infection rate (%/day)', fontsize=font_size)
        ax.set_xticks(x_ticks)
        ax.xaxis.set_minor_locator(ticker.FixedLocator([day_x[point_ss]]))
        ax.xaxis.set_minor_formatter(ticker.ScalarFormatter())
        ax.tick_params(which='minor', length=17, color='b', labelsize=13)
        ax.tick_params(labelsize=15)
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)
        ax.grid(True, lw=1, ls='--', c='.75')

        # infection rate control
        ax = axes[2]
        ax.set_title('infection rate control over days', loc='left', fontsize=font_size)
        ax.plot(day_x[:point_ss + 1], self.infection_control_curve_[:point_ss + 1],
                **plot_curve_args[0])
        ax.plot(day_x[point_ss:], self.infection_control_curve_[point_ss:],
                **plot_curve_args[1])
        y_min = ax.get_ylim()[0]
        ax.plot([day_x[point_ss]] * 2,
                [y_min, self.infection_control_curve_[point_ss]],
                **plot_vert_args[2])

        ax.set_xlabel(xlabel='day', fontsize=font_size)
        ax.set_ylabel(ylabel='infection rate control (%/day)', fontsize=font_size)
        ax.set_xticks(x_ticks)
        ax.xaxis.set_minor_locator(ticker.FixedLocator([day_x[point_ss]]))
        ax.xaxis.set_minor_formatter(ticker.ScalarFormatter())
        ax.tick_params(which='minor', length=17, color='b', labelsize=13)
        ax.tick_params(labelsize=15)
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=y_min)
        ax.grid(True, lw=1, ls='--', c='.75')

        if show_plot:
            plt.show()

        fig.savefig(os.path.join(save_dir, filename + '.png'))