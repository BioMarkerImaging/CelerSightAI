"""
This is a handler for the size of the dock widgets

"""
class DockSizeHandler(object):
    def __init__(self, MainWindowUi = None):
        super(DockSizeHandler, self).__init__()
        self.MainWindowUi = MainWindowUi
        #
        # Get initial values for Docks
        #
        self.PlotSetMinW = self.MainWindowUi.plot_dools_dock.minimumWidth()
        self.PlotSetMinH = self.MainWindowUi.plot_dools_dock.minimumHeight()

        self.PlotMinW = self.MainWindowUi.plot_dock.minimumWidth()
        self.PlotMinH = self.MainWindowUi.plot_dock.minimumHeight()

        self.MainWindowUi.plot_dools_dock.setMinimumHeight(400)
        self.MainWindowUi.plot_dock.setMinimumHeight(200)
        # self.MainWindowUi.canvas.setMinimumSize(QtCore.QSize(116, 700)) # TODO: maybe change this?

    # def GetInitialSizes(self):
