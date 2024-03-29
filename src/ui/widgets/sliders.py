
__all__ = ['DoubleSlider', 'RangeSlider']

'''
Source: https://gist.github.com/dennis-tra/994a65d6165a328d4eabaadbaedac2cc
'''

import logging
import sys

from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtWidgets import QSlider

from src.utils.helpers import print_exception

logger = logging.getLogger(__name__)


class DoubleSlider(QSlider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.decimals = 5
        self._max_int = 10 ** self.decimals

        # # super().setMinimum(0)
        # super().setMinimum(0)
        # super().setMaximum(self._max_int)
        #
        # # self._min_value = 0.0
        # self._min_value = 0.001
        # self._max_value = 1.0
        #

        # Set integer max and min. These stay constant.
        super().setMinimum(0)
        self._max_int = 10000
        super().setMaximum(self._max_int)

        # The "actual" min and max values seen by user
        self._min_value = 0.0
        self._max_value = 100.0

    @property
    def _value_range(self):
        return self._max_value - self._min_value

    # def value(self):
    #     return float(super().value()) / self._max_int * self._value_range
    #
    # def setValue(self, value):
    #     logger.info(f'value = {value}')
    #     super().setValue(int(value / self._value_range * self._max_int))

    def value(self):
        return float(super().value()) / self._max_int * self._value_range + self._min_value
        # return float(super().value()) / self._max_int * self._value_range + self._min_value

    def setValue(self, value):
        try:
            super().setValue(int((value - self._min_value) / self._value_range * self._max_int))
            # super().setValue(float((value - self._min_value) / self._value_range * self._max_int))
        except:
            super().setValue(10)
            logger.warning('Unable to set wSlider value to %s' %str(value))
            # print_exception()


    def setMinimum(self, value):
        if value > self._max_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._min_value = value
        self.setValue(self.value())

    def setMaximum(self, value):
        if value < self._min_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._max_value = value
        self.setValue(self.value())

    def minimum(self):
        return self._min_value

    def maximum(self):
        return self._max_value



# class DoubleSlider(QSlider):
#
#     # create our our signal that we can connect to if necessary
#     doubleValueChanged = Signal(float)
#
#     def __init__(self, decimals=3, *args, **kargs):
#         super(DoubleSlider, self).__init__( *args, **kargs)
#         self._multi = 10 ** decimals
#         self.valueChanged.connect(self.emitDoubleValueChanged)
#
#     def emitDoubleValueChanged(self):
#         value = float(super(DoubleSlider, self).value())/self._multi
#         self.doubleValueChanged.emit(value)
#
#     def value(self):
#         return float(super(DoubleSlider, self).value()) / self._multi
#
#     def setMinimum(self, value):
#         return super(DoubleSlider, self).setMinimum(value * self._multi)
#
#     def setMaximum(self, value):
#         return super(DoubleSlider, self).setMaximum(value * self._multi)
#
#     def setSingleStep(self, value):
#         return super(DoubleSlider, self).setSingleStep(value * self._multi)
#
#     def singleStep(self):
#         return float(super(DoubleSlider, self).singleStep()) / self._multi
#
#     def setValue(self, value):
#         super(DoubleSlider, self).setValue(int(value * self._multi))

'''Source:
https://stackoverflow.com/questions/47342158/porting-range-slider-widget-to-pyqt5'''

DEFAULT_CSS = """
RangeSlider * { border: 0px; padding: 0px; font-size: 7px;}
RangeSlider #Head { background: #194d19; }
RangeSlider #Tail { background: #194d19; } 
RangeSlider #Span { background: #8bb8e8; }
RangeSlider #Span:active { background: #00FF00; }
RangeSlider > QSplitter::handle { background: #f3f6fb; }
RangeSlider > QSplitter::handle:vertical { height: 4px; }
RangeSlider > QSplitter::handle:pressed { background: #339933; }
"""

def scale(val, src, dst):
    try:
        return int(((val - src[0]) / float(src[1]-src[0])) * (dst[1]-dst[0]) + dst[0])
    except ZeroDivisionError:
        logger.warning('cannot divide by 0')


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("RangeSlider")
        Form.resize(300, 30)
        Form.setStyleSheet(DEFAULT_CSS)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self._splitter = QtWidgets.QSplitter(Form)
        self._splitter.setMinimumSize(QtCore.QSize(0, 0))
        self._splitter.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self._splitter.setOrientation(QtCore.Qt.Horizontal)
        self._splitter.setObjectName("splitter")
        self._head = QtWidgets.QGroupBox(self._splitter)
        self._head.setTitle("")
        self._head.setObjectName("Head")
        self._handle = QtWidgets.QGroupBox(self._splitter)
        self._handle.setTitle("")
        self._handle.setObjectName("Span")
        self._tail = QtWidgets.QGroupBox(self._splitter)
        self._tail.setTitle("")
        self._tail.setObjectName("Tail")
        self.gridLayout.addWidget(self._splitter, 0, 0, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("RangeSlider", "RangeSlider"))


class Element(QtWidgets.QGroupBox):
    def __init__(self, parent, main):
        super(Element, self).__init__(parent)
        self.main = main

    def setStyleSheet(self, style):
        self.parent().setStyleSheet(style)

    def textColor(self):
        return getattr(self, '__textColor', QtGui.QColor('#969696'))

    def setTextColor(self, color):
        if type(color) == tuple and len(color) == 3:
            color = QtGui.QColor(color[0], color[1], color[2])
        elif type(color) == int:
            color = QtGui.QColor(color, color, color)
        setattr(self, '__textColor', color)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.main.drawValues():
            self.drawText(event, qp)
        qp.end()


class Head(Element):
    def __init__(self, parent, main):
        super(Head, self).__init__(parent, main)

    def drawText(self, event, qp):
        qp.setPen(self.textColor())
        qp.setFont(QtGui.QFont('Arial', 10))
        qp.drawText(event.rect(), QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, str(self.main.min()))


class Tail(Element):
    def __init__(self, parent, main):
        super(Tail, self).__init__(parent, main)

    def drawText(self, event, qp):
        qp.setPen(self.textColor())
        qp.setFont(QtGui.QFont('Arial', 10))
        qp.drawText(event.rect(), QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom, str(self.main.max()))


class Handle(Element):
    def __init__(self, parent, main):
        super(Handle, self).__init__(parent, main)

    def drawText(self, event, qp):
        qp.setPen(self.textColor())
        qp.setFont(QtGui.QFont('Arial', 10))
        qp.drawText(event.rect(), QtCore.Qt.AlignLeft  | QtCore.Qt.AlignTop, str(self.main.start()))
        qp.drawText(event.rect(), QtCore.Qt.AlignRight  | QtCore.Qt.AlignBottom, str(self.main.end()))

    def mouseMoveEvent(self, event):
        event.accept()
        mx = event.globalX()
        _mx = getattr(self, '__mx', None)
        if not _mx:
            setattr(self, '__mx', mx)
            dx = 0
        else:
            dx = mx - _mx
        setattr(self, '__mx', mx)
        if dx == 0:
            event.ignore()
            return
        elif dx > 0:
            dx = 1
        elif dx < 0:
            dx = -1
        s = self.main.start() + dx
        e = self.main.end() + dx
        if s >= self.main.min() and e <= self.main.max():
            self.main.setRange(s, e)


class RangeSlider(QtWidgets.QWidget, Ui_Form):
    endValueChanged = QtCore.Signal(int)
    maxValueChanged = QtCore.Signal(int)
    minValueChanged = QtCore.Signal(int)
    startValueChanged = QtCore.Signal(int)

    _SPLIT_START = 1
    _SPLIT_END = 2

    def __init__(self, parent=None):
        super(RangeSlider, self).__init__(parent)
        self.setupUi(self)
        self.setMouseTracking(False)
        self._splitter.splitterMoved.connect(self._handleMoveSplitter)
        self._head_layout = QtWidgets.QHBoxLayout()
        self._head_layout.setSpacing(0)
        self._head_layout.setContentsMargins(0, 0, 0, 0)
        self._head.setLayout(self._head_layout)
        self.head = Head(self._head, main=self)
        self._head_layout.addWidget(self.head)
        self._handle_layout = QtWidgets.QHBoxLayout()
        self._handle_layout.setSpacing(0)
        self._handle_layout.setContentsMargins(0, 0, 0, 0)
        self._handle.setLayout(self._handle_layout)
        self.handle = Handle(self._handle, main=self)
        # self.handle.setTextColor(QtGui.QColor('#1b1e23'))
        self.handle.setTextColor(QtGui.QColor(QtCore.Qt.white))
        self._handle_layout.addWidget(self.handle)
        self._tail_layout = QtWidgets.QHBoxLayout()
        self._tail_layout.setSpacing(0)
        self._tail_layout.setContentsMargins(0, 0, 0, 0)
        self._tail.setLayout(self._tail_layout)
        self.tail = Tail(self._tail, main=self)
        self._tail_layout.addWidget(self.tail)
        self.setMin(0)
        self.setMax(99)
        self.setStart(0)
        self.setEnd(99)
        self.setDrawValues(True)

    def min(self):
        return getattr(self, '__min', None)

    def max(self):
        return getattr(self, '__max', None)

    def setMin(self, value):
        setattr(self, '__min', value)
        self.minValueChanged.emit(value)

    def setMax(self, value):
        setattr(self, '__max', value)
        self.maxValueChanged.emit(value)

    def start(self):
        return getattr(self, '__start', None)

    def end(self):
        return getattr(self, '__end', None)

    def _setStart(self, value):
        setattr(self, '__start', value)
        self.startValueChanged.emit(value)

    def setStart(self, value):
        v = self._valueToPos(value)
        self._splitter.splitterMoved.disconnect()
        self._splitter.moveSplitter(v, self._SPLIT_START)
        self._splitter.splitterMoved.connect(self._handleMoveSplitter)
        self._setStart(value)

    def _setEnd(self, value):
        setattr(self, '__end', value)
        self.endValueChanged.emit(value)

    def setEnd(self, value):
        v = self._valueToPos(value)
        self._splitter.splitterMoved.disconnect()
        self._splitter.moveSplitter(v, self._SPLIT_END)
        self._splitter.splitterMoved.connect(self._handleMoveSplitter)
        self._setEnd(value)

    def drawValues(self):
        return getattr(self, '__drawValues', None)

    def setDrawValues(self, draw):
        setattr(self, '__drawValues', draw)

    def getRange(self):
        return (self.start(), self.end())

    def setRange(self, start, end):
        self.setStart(start)
        self.setEnd(end)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Left:
            s = self.start()-1
            e = self.end()-1
        elif key == QtCore.Qt.Key_Right:
            s = self.start()+1
            e = self.end()+1
        else:
            event.ignore()
            return
        event.accept()
        if s >= self.min() and e <= self.max():
            self.setRange(s, e)

    def setBackgroundStyle(self, style):
        self._tail.setStyleSheet(style)
        self._head.setStyleSheet(style)

    def setSpanStyle(self, style):
        self._handle.setStyleSheet(style)

    def _valueToPos(self, value):
        return scale(value, (self.min(), self.max()), (0, self.width()))

    def _posToValue(self, xpos):
        return scale(xpos, (0, self.width()), (self.min(), self.max()))

    def _handleMoveSplitter(self, xpos, index):
        hw = self._splitter.handleWidth()
        def _lockWidth(widget):
            width = widget.size().width()
            widget.setMinimumWidth(width)
            widget.setMaximumWidth(width)
        def _unlockWidth(widget):
            widget.setMinimumWidth(0)
            widget.setMaximumWidth(16777215)
        # v = self._posToValue(xpos)
        if index == 1:
            v = self._posToValue(xpos)
        elif index == 2:
            v = self._posToValue(xpos + hw)

        if index == self._SPLIT_START:
            _lockWidth(self._tail)
            if v >= self.end():
                return
            offset = -20
            w = xpos + offset
            self._setStart(v)
        elif index == self._SPLIT_END:
            _lockWidth(self._head)
            if v <= self.start():
                return
            offset = -40
            w = self.width() - xpos + offset
            self._setEnd(v)
        _unlockWidth(self._tail)
        _unlockWidth(self._head)
        _unlockWidth(self._handle)










class DoubleSlider(QSlider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set integer max and min. These stay constant.
        super().setMinimum(0)
        self._max_int = 10000
        super().setMaximum(self._max_int)

        # The "actual" min and max values seen by user
        self._min_value = 0.0
        self._max_value = 100.0

    @property
    def _value_range(self):
        return self._max_value - self._min_value

    def setMinimum(self, value):
        self.setRange(value, self._max_value)

    def setMaximum(self, value):
        self.setRange(self._min_value, value)

    def setRange(self, minimum, maximum):
        old_value = self.value()
        self._min_value = minimum
        self._max_value = maximum
        self.setValue(old_value)  # Put wSlider in correct position

    def value(self):
        return float(super().value()) / self._max_int * self._value_range

    def setValue(self, value):
        if value not in range(int(self._min_value), int(self._max_value)):
            return
        try:
            super().setValue(int(value / self._value_range * self._max_int))
        except:
            print_exception()
            logger.warning(f'value: {value} ; self._value_range: {str(self._value_range)} ; self._max_int: {str(self._max_int)}')
            logger.warning(f'current value: {self.value()}')

    def proportion(self):
        return (self.value() - self._min_value) / self._value_range

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    rs = RangeSlider()
    rs.show()
    rs.setRange(15, 35)
    rs.setBackgroundStyle('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #222, stop:1 #333);')
    rs.handle.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #282, stop:1 #393);')
    app.exec_()