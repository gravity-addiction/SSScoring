# See: https://github.com/pr3d4t0r/SSScoring/blob/master/LICENSE.txt

"""
## Utility reusable code for notebooks.
"""


from bokeh.models import LinearAxis
from bokeh.models import Range1d

from ssscoring.constants import MAX_ALTITUDE_FT

import bokeh.io as bi
import bokeh.plotting as bp


# *** constants ***
DATA_LAKE_ROOT = './data' # Lucyfer default
SPEED_COLORS = colors = ('limegreen', 'blue', 'tomato', 'turquoise', 'deepskyblue', 'forestgreen', 'coral', 'darkcyan',)


# *** global initialization ***

bp.output_notebook(hide_banner = True)
# TODO: make this configurable:
bi.curdoc().theme = 'dark_minimal'


# *** functions ***

def initializePlot(jumpTitle: str,
                   height = 500,
                   width = 900,
                   xLabel = 'seconds from exit',
                   yLabel = 'km/h',
                   # TODO: roll back to 40.0?
                   # xMax = 40.0,
                   xMax = 35.0,
                   yMax = 550.0):
    """
    Initiialize a plotting area for notebook output.

    Arguments
    ---------
        jumpTitle: str
    A title to identify the plot.

        height: int
    Height of the plot in pixels.  Default = 500.

        width: int
    Width of the plot in pixels.  Default = 900.

        xLabel: str
    X axis label.  Default:  `'seconds from exit'`

        yLabel: str
    Y axis label.  Default:  `'km/h'`

        xMax: float
    The maximum rnage for the X axis.  Default = 40.0

        yMax: float
    The maximum range for the Y axis.  Default = 550
    """
    return bp.figure(title = jumpTitle,
                     height = height,
                     width = width,
                     x_axis_label = xLabel,
                     y_axis_label = yLabel,
                     x_range = (0.0, xMax),
                     y_range = (0.0, yMax))


def _graphSegment(plot,
                  x0 = 0.0,
                  y0 = 0.0,
                  x1 = 0.0,
                  y1 = 0.0,
                  lineWidth = 1,
                  color = 'black'):
    plot.segment(x0 = [ x0, ],
                 y0 = [ y0, ],
                 x1 = [ x1, ],
                 y1 = [ y1, ],
                 line_width = lineWidth,
                 color = color)


def initializeExtraYRanges(plot,
                           startY: float = 0.0,
                           endY: float = MAX_ALTITUDE_FT):
    """
    Initialize an extra Y range for reporting other data trend (e.g. altitude)
    in the plot.

    Arguments
    ---------
        plot
    A valid instance of `bp.figure` with an existing plot defined for it

        startY: float
    The Y range starting value

        endY: float
    The Y range ending value

    Returns
    -------
    An instance of `bp.figure` updated to report an additional Y axis.
    """
    plot.extra_y_ranges = {
        'altitudeFt': Range1d(start = startY, end = endY),
        'angle': Range1d(start = 0.0, end = 90.0),
    }
    plot.add_layout(LinearAxis(y_range_name = 'altitudeFt', axis_label = 'Alt (ft)'), 'left')
    plot.add_layout(LinearAxis(y_range_name = 'angle', axis_label = 'angle'), 'left')

    return plot


def graphJumpResult(plot,
                    jumpResult,
                    lineColor = 'green',
                    legend = 'speed',
                    showIt = True):
    """
    Graph the jump results using the initialized plot.

    Arguments
    ---------
        plot: bp.figure
    A Bokeh figure where to render the plot.

        jumpResult: ssscoring.JumpResults
    A jump results named tuple with score, max speed, scores, data, etc.

        lineColor: str
    A valid color from the Bokeh palette:  https://docs.bokeh.org/en/2.1.1/docs/reference/colors.html
    This module defines 8 colors for rendering a competition's results.  See:
    `ssscoring.notebook.SPEED_COLORS` for the list.

        leged: str
    A title for the plot.

        showIt: bool
    A boolean flag for whether the call should render the plot upon the function
    call.  This flag is used for combining two or more jumps on the same plot.
    In that case, a call to this function is made with a different `jumpResult`
    and the `showIt` flag set to `False`.  When the user is ready to view the
    combined plot, issue a call to `bp.show(plot)`.  Example:

    ```python
    for result in jumpResults:
        graphJumpResult(plot, result, showIt = False)

    bp.show(plot)

    Returns
    -------
    `None`.
    ```
    """
    data = jumpResult.data
    scores = jumpResult.scores
    score = jumpResult.score
    plot.line(data.plotTime, data.vKMh, legend_label = legend, line_width = 2, line_color = lineColor)

    if showIt:
        plot.line(data.plotTime, data.hKMh, legend_label = 'H-speed', line_width = 2, line_color = 'red')
        _graphSegment(plot, scores[score], 0.0, scores[score], score, 3, 'lightblue')
        _graphSegment(plot, scores[score]+1.5, 0.0, scores[score]+1.5, score, 1, 'darkseagreen')
        _graphSegment(plot, scores[score]-1.5, 0.0, scores[score]-1.5, score, 1, 'darkseagreen')
        plot.scatter(x = [ scores[score], ], y = [ score, ], marker = 'square_cross', size = [ 20, ], line_color = 'lightblue', fill_color = None, line_width = 3)
        bp.show(plot)


def graphAltitude(plot,
                  jumpResult,
                  label = 'Alt (ft)',
                  lineColor = 'palegoldenrod',
                  rangeName = 'altitudeFt'):
    """
    Graph a vertical axis with additional data, often used for altitude in ft
    ASL.

    Arguments
    ---------
        plot: pb.figure
    A Bokeh figure where to render the plot.

        jumpResult: ssscoring.JumpResults
    A jump results named tuple with score, max speed, scores, data, etc.

        label: str
    The legend label for the new Y axis.

        lineColor: str
    A color name from the Bokeh palette.

        rangeName: str
    The range name to associate the `LinearAxis` layout with the data for
    plotting.

    Returns
    -------
    `None`.
    """
    data = jumpResult.data
    plot.line(data.plotTime, data.altitudeASLFt, legend_label = label, line_width = 2, line_color = lineColor, y_range_name = rangeName)


def graphAngle(plot,
               jumpResult,
               label = 'angle',
               lineColor = 'deepskyblue',
               rangeName = 'angle'):
    """
    Graph the flight angle

    Arguments
    ---------
        plot: pb.figure
    A Bokeh figure where to render the plot.

        jumpResult: ssscoring.JumpResults
    A jump results named tuple with score, max speed, scores, data, etc.

        label: str
    The legend label for the new Y axis.

        lineColor: str
    A color name from the Bokeh palette.

        rangeName: str
    The range name to associate the `LinearAxis` layout with the data for
    plotting.

    Returns
    -------
    `None`.
    """
    data = jumpResult.data
    plot.line(data.plotTime, data.speedAngle, legend_label = label, line_width = 2, line_color = lineColor, y_range_name = rangeName)

