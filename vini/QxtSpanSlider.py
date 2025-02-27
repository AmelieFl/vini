# The MIT License (MIT)

# Copyright (c) 2011-2014 Marvin Killing

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

try:
    from PyQt6.QtWidgets import (QApplication,
                                QAbstractSlider, QSlider,
                                QStyle, QStylePainter, QStyleOptionSlider)
    from PyQt6.QtGui import QPalette, QLinearGradient, QPen, QColor
    from PyQt6.QtCore import (Qt, 
                            QRect, QRectF, QPoint,
                            pyqtSignal as Signal, pyqtProperty as Property)
except ImportError:
    from PyQt5.QtWidgets import (QApplication,
                                QAbstractSlider, QSlider,
                                QStyle, QStylePainter, QStyleOptionSlider)
    from PyQt5.QtGui import QPalette, QLinearGradient, QPen, QColor
    from PyQt5.QtCore import (Qt, 
                            QRect, QRectF, QPoint,
                            pyqtSignal as Signal, pyqtProperty as Property) 

#qtpy can also be used
#from qtpy.QtWidgets import (QApplication,
#                            QAbstractSlider, QSlider,
#                            QStyle, QStylePainter, QStyleOptionSlider)
#from qtpy.QtGui import QPalette, QLinearGradient, QPen, QColor
#from qtpy.QtCore import (Qt, 
#                         QRect, QRectF, QPoint,
#                         Signal, Property)

def clamp(v, lower, upper):
    return min(upper, max(lower, v))

class QxtSpanSlider(QSlider):
    NoHandle = None
    LowerHandle = 1
    UpperHandle = 2
    
    FreeMovement = None
    NoCrossing = 1
    NoOverlapping = 2
    
    spanChanged = Signal(int, int)
    lowerValueChanged = Signal(int)
    upperValueChanged = Signal(int)
    lowerPositionChanged = Signal(int)
    upperPositionChanged = Signal(int)
    sliderPressed = Signal(object)

    def __init__(self, parent = None):
        QSlider.__init__(self, Qt.Orientation.Horizontal, parent)
        self.rangeChanged.connect(self.updateRange)
        self.sliderReleased.connect(self.movePressedHandle)

        self.lower = 0
        self.upper = 0
        self.lowerPos = 0
        self.upperPos = 0
        self.offset = 0
        self.position = 0
        self.lastPressed = QxtSpanSlider.NoHandle
        self.upperPressed = QStyle.SubControl.SC_None
        self.lowerPressed = QStyle.SubControl.SC_None
        self.movement = QxtSpanSlider.FreeMovement
        self.mainControl = QxtSpanSlider.LowerHandle
        self.firstMovement = False
        self.blockTracking = False
        self.gradientLeft = self.palette().color(QPalette.ColorRole.Dark).lighter(110)
        self.gradientRight = self.palette().color(QPalette.ColorRole.Dark).lighter(110)
        

    @Property(int)
    def lowerValue(self):
        return min(self.lower, self.upper)
        
    
    def setLowerValue(self, lower):
        self.setSpan(lower, self.upper)
        
    
    @Property(int)
    def upperValue(self):
        return max(self.lower, self.upper)
        
       
    def setUpperValue(self, upper):
        self.setSpan(self.lower, upper)
        

    @Property(object)
    def handleMovementMode(self):
        return self.movement
        
    
    def setHandleMovementMode(self, mode):
        self.movement = mode
        

    def setSpan(self, lower, upper):
        low = clamp(min(lower, upper), self.minimum(), self.maximum())
        upp = clamp(max(lower, upper), self.minimum(), self.maximum())
        changed = False
        if low != self.lower:
            self.lower = low
            self.lowerPos = low
            changed = True
        if upp != self.upper:
            self.upper = upp
            self.upperPos = upp
            changed = True
        if changed:
            self.spanChanged.emit(self.lower, self.upper)
            self.update()


    @Property(int)
    def lowerPosition(self):
        return self.lowerPos
        

    def setLowerPosition(self, lower):
        if self.lowerPos != lower:
            self.lowerPos = lower
            if not self.hasTracking():
                self.update()
            if self.isSliderDown():
                self.lowerPositionChanged.emit(lower)
            if self.hasTracking() and not self.blockTracking:
                main = (self.mainControl == QxtSpanSlider.LowerHandle)
                self.triggerAction(QxtSpanSlider.SliderAction.SliderMove, main)
                

    @Property(int)
    def upperPosition(self):
        return self.upperPos
        

    def setUpperPosition(self, upper):
        if self.upperPos != upper:
            self.upperPos = upper
            if not self.hasTracking():
                self.update()
            if self.isSliderDown():
                self.upperPositionChanged.emit(upper)
            if self.hasTracking() and not self.blockTracking:
                main = (self.mainControl == QxtSpanSlider.UpperHandle)
                self.triggerAction(QxtSpanSlider.SliderAction.SliderMove, main)
             
             
    @Property(object)
    def gradientLeftColor(self):
        return self.gradientLeft
        
        
    def setGradientLeftColor(self, color):
        self.gradientLeft = color
        self.update()
        
        
    @Property(object)
    def gradientRightColor(self):
        return self.gradientRight
      
      
    def setGradientRightColor(self, color):
        self.gradientRight = color
        self.update()
        
    
    def movePressedHandle(self):
        if self.lastPressed == QxtSpanSlider.LowerHandle:
            if self.lowerPos != self.lower:
                main = (self.mainControl == QxtSpanSlider.LowerHandle)
                self.triggerAction(QAbstractSlider.SliderAction.SliderMove, main)
        elif self.lastPressed == QxtSpanSlider.UpperHandle:
            if self.upperPos != self.upper:
                main = (self.mainControl == QxtSpanSlider.UpperHandle)
                self.triggerAction(QAbstractSlider.SliderAction.SliderMove, main)
                

    def pick(self, p):
        if self.orientation() == Qt.Orientation.Horizontal:
            return p.x()
        else:
            return p.y()
            
    
    def triggerAction(self, action, main):
        value = 0
        no = False
        up = False
        my_min = self.minimum()
        my_max = self.maximum()
        altControl = QxtSpanSlider.LowerHandle
        if self.mainControl == QxtSpanSlider.LowerHandle:
            altControl = QxtSpanSlider.UpperHandle

        self.blockTracking = True
        
        isUpperHandle = (main and self.mainControl == QxtSpanSlider.UpperHandle) or (not main and altControl == QxtSpanSlider.UpperHandle)
        
        if action == QAbstractSlider.SliderAction.SliderSingleStepAdd:
            if isUpperHandle:
                value = clamp(self.upper + self.singleStep(), my_min, my_max)
                up = True
            else:
                value = clamp(self.lower + self.singleStep(), my_min, my_max)
        elif action == QAbstractSlider.SliderAction.SliderSingleStepSub:
            if isUpperHandle:
                value = clamp(self.upper - self.singleStep(), my_min, my_max)
                up = True
            else:
                value = clamp(self.lower - self.singleStep(), my_min, my_max)
        elif action == QAbstractSlider.SliderAction.SliderToMinimum:
            value = my_min
            if isUpperHandle:
                up = True
        elif action == QAbstractSlider.SliderAction.SliderToMaximum:
            value = my_max
            if isUpperHandle:
                up = True
        elif action == QAbstractSlider.SliderAction.SliderMove:
            if isUpperHandle:
                up = True
            no = True
        elif action == QAbstractSlider.SliderNoAction:
            no = True

        if not no and not up:
            if self.movement == QxtSpanSlider.NoCrossing:
                value = min(value, self.upper)
            elif self.movement == QxtSpanSlider.NoOverlapping:
                value = min(value, self.upper - 1)

            if self.movement == QxtSpanSlider.FreeMovement and value > self.upper:
                self.swapControls()
                self.setUpperPosition(value)
            else:
                self.eetLowerPosition(value)
        elif not no:
            if self.movement == QxtSpanSlider.NoCrossing:
                value = max(value, self.lower)
            elif self.movement == QxtSpanSlider.NoOverlapping:
                value = max(value, self.lower + 1)

            if self.movement == QxtSpanSlider.FreeMovement and value < self.lower:
                self.swapControls()
                self.setLowerPosition(value)
            else:
                self.setUpperPosition(value)

        self.blockTracking = False
        self.setLowerValue(self.lowerPos)
        self.setUpperValue(self.upperPos)
        
    
    def swapControls(self):
        self.lower, self.upper = self.upper, self.lower
        self.lowerPressed, self.upperPressed = self.upperPressed, self.lowerPressed

        if self.lastPressed == QxtSpanSlider.LowerHandle:
            self.lastPressed = QxtSpanSlider.UpperHandle
        else:
            self.lastPressed = QxtSpanSlider.LowerHandle
            
        if self.mainControl == QxtSpanSlider.LowerHandle:
            self.mainControl = QxtSpanSlider.UpperHandle
        else:
            self.mainControl = QxtSpanSlider.LowerHandle
            

    def updateRange(self, min, max):
        # setSpan() takes care of keeping span in range
        self.setSpan(self.lower, self.upper)
        
    
    def paintEvent(self, event):
        painter = QStylePainter(self)
        
        # ticks
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        opt.subControls = QStyle.SubControl.SC_SliderTickmarks
        painter.drawComplexControl(QStyle.ComplexControl.CC_Slider, opt)

        # groove
        opt.sliderPosition = 00
        opt.sliderValue = 0
        opt.subControls = QStyle.SubControl.SC_SliderGroove
        painter.drawComplexControl(QStyle.ComplexControl.CC_Slider, opt)

        # handle rects
        opt.sliderPosition = self.lowerPos
        lr = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt, QStyle.SubControl.SC_SliderHandle, self)
        lrv  = self.pick(lr.center())
        opt.sliderPosition = self.upperPos
        ur = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt, QStyle.SubControl.SC_SliderHandle, self)
        urv  = self.pick(ur.center())

        # span
        minv = min(lrv, urv)
        maxv = max(lrv, urv)
        c = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt, QStyle.SubControl.SC_SliderGroove, self).center()
        spanRect = QRect(QPoint(c.x() - 2, minv), QPoint(c.x() + 1, maxv))
        if self.orientation() == Qt.Orientation.Horizontal:
            spanRect = QRect(QPoint(minv, c.y() - 2), QPoint(maxv, c.y() + 1))
        self.drawSpan(painter, spanRect)

        # handles
        if self.lastPressed == QxtSpanSlider.LowerHandle:
            self.drawHandle(painter, QxtSpanSlider.UpperHandle)
            self.drawHandle(painter, QxtSpanSlider.LowerHandle)
        else:
            self.drawHandle(painter, QxtSpanSlider.LowerHandle)
            self.drawHandle(painter, QxtSpanSlider.UpperHandle)
            

    def setupPainter(self, painter, orientation, x1, y1, x2, y2):
        highlight = self.palette().color(QPalette.ColorRole.Highlight)
        gradient = QLinearGradient(x1, y1, x2, y2)
        gradient.setColorAt(0, highlight.darker(120))
        gradient.setColorAt(1, highlight.lighter(108))
        painter.setBrush(gradient)

        if orientation == Qt.Orientation.Horizontal:
            painter.setPen(QPen(highlight.darker(130), 0))
        else:
            painter.setPen(QPen(highlight.darker(150), 0))
            

    def drawSpan(self, painter, rect):
        opt = QStyleOptionSlider()
        QSlider.initStyleOption(self, opt)

        # area
        groove = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt, QStyle.SubControl.SC_SliderGroove, self)
        if opt.orientation == Qt.Orientation.Horizontal:
            groove.adjust(0, 0, -1, 0);
        else:
            groove.adjust(0, 0, 0, -1);

        # pen & brush
        painter.setPen(QPen(self.gradientLeftColor, 0))
        if opt.orientation == Qt.Orientation.Horizontal:
            self.setupPainter(painter, opt.orientation, groove.center().x(), groove.top(), groove.center().x(), groove.bottom())
        else:
            self.setupPainter(painter, opt.orientation, groove.left(), groove.center().y(), groove.right(), groove.center().y())


        # draw groove
        intersected = QRectF(rect.intersected(groove))
        gradient = QLinearGradient(intersected.topLeft(), intersected.topRight())
        gradient.setColorAt(0, self.gradientLeft)
        gradient.setColorAt(1, self.gradientRight)
        
        
        painter.fillRect(intersected, gradient)
        
    
    def drawHandle(self, painter, handle):
        opt = QStyleOptionSlider()
        self._initStyleOption(opt, handle)
        opt.subControls = QStyle.SubControl.SC_SliderHandle
        pressed = self.upperPressed
        if handle == QxtSpanSlider.LowerHandle:
            pressed = self.lowerPressed
        
        if pressed == QStyle.SubControl.SC_SliderHandle:
            opt.activeSubControls = pressed
            opt.state |= QStyle.StateFlag.State_Sunken
        painter.drawComplexControl(QStyle.ComplexControl.CC_Slider, opt)
        
    
    def _initStyleOption(self, option, handle):
        self.initStyleOption(option)

        option.sliderPosition = self.upperPos
        if handle == QxtSpanSlider.LowerHandle:
            option.sliderPosition = self.lowerPos

        option.sliderValue = self.upper
        if handle == QxtSpanSlider.LowerHandle:
            option.sliderPosition = self.lower
            
    
    def handleMousePress(self, pos, control, value, handle):
        opt = QStyleOptionSlider()
        self._initStyleOption(opt, handle)
        oldControl = control
        control = self.style().hitTestComplexControl(QStyle.ComplexControl.CC_Slider, opt, pos, self)
        sr = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt, QStyle.SubControl.SC_SliderHandle, self)
        if control == QStyle.SubControl.SC_SliderHandle:
            self.position = value
            self.offset = self.pick(pos - sr.topLeft())
            self.lastPressed = handle
            self.setSliderDown(True)
            self.sliderPressed.emit(handle)
        if control != oldControl:
            self.update(sr)
        return control
        
    
    def mousePressEvent(self, event):
        if self.minimum() == self.maximum() or event.buttons() ^ event.button():
            event.ignore()
            return

        self.upperPressed = self.handleMousePress(event.pos(), self.upperPressed, self.upper, QxtSpanSlider.UpperHandle)
        if self.upperPressed != QStyle.SubControl.SC_SliderHandle:
            self.lowerPressed = self.handleMousePress(event.pos(), self.lowerPressed, self.lower, QxtSpanSlider.LowerHandle)

        self.firstMovement = True
        event.accept()
        
    
    def mouseMoveEvent(self, event):
        if self.lowerPressed != QStyle.SubControl.SC_SliderHandle and self.upperPressed != QStyle.SubControl.SC_SliderHandle:
            event.ignore()
            return

        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        m = self.style().pixelMetric(QStyle.PixelMetric.PM_MaximumDragDistance, opt, self)
        newPosition = self.pixelPosToRangeValue(self.pick(event.pos()) - self.offset)
        if m >= 0:
            r = self.rect().adjusted(-m, -m, m, m)
            if not r.contains(event.pos()):
                newPosition = self.position

        # pick the preferred handle on the first movement
        if self.firstMovement:
            if self.lower == self.upper:
                if newPosition < self.lowerValue:
                    self.swapControls()
                    self.firstMovement = False
            else:
                self.firstMovement = False

        if self.lowerPressed == QStyle.SubControl.SC_SliderHandle:
            if self.movement == QxtSpanSlider.NoCrossing:
                newPosition = min(newPosition, self.upper)
            elif self.movement == QxtSpanSlider.NoOverlapping:
                newPosition = min(newPosition, self.upper - 1)

            if self.movement == QxtSpanSlider.FreeMovement and newPosition > self.upper:
                self.swapControls()
                self.setUpperPosition(newPosition)
            else:
                self.setLowerPosition(newPosition)
        elif self.upperPressed == QStyle.SubControl.SC_SliderHandle:
            if self.movement == QxtSpanSlider.NoCrossing:
                newPosition = max(newPosition, self.lowerValue)
            elif self.movement == QxtSpanSlider.NoOverlapping:
                newPosition = max(newPosition, self.lowerValue + 1);

            if self.movement == QxtSpanSlider.FreeMovement and newPosition < self.lower:
                self.swapControls()
                self.setLowerPosition(newPosition)
            else:
                self.setUpperPosition(newPosition)
        event.accept()
        
    
    def mouseReleaseEvent(self, event):
        QSlider.mouseReleaseEvent(self, event)
        self.setSliderDown(False)
        self.lowerPressed = QStyle.SubControl.SC_None
        self.upperPressed = QStyle.SubControl.SC_None
        self.update()
        
    
    def pixelPosToRangeValue(self, pos):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)

        sliderMin = 0
        sliderMax = 0
        sliderLength = 0
        gr = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt, QStyle.SubControl.SC_SliderGroove, self)
        sr = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt, QStyle.SubControl.SC_SliderHandle, self)
        if self.orientation() == Qt.Orientation.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1
        
        return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), pos - sliderMin, sliderMax - sliderMin, opt.upsideDown)

    
if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    slider = QxtSpanSlider()
    slider.setSpan(30, 70)
    slider.setRange(0, 100)
    color = QColor(Qt.blue).lighter(0)
    slider.setGradientLeftColor(color)
    slider.setGradientRightColor(color)
    slider.show()
    sys.exit(app.exec())
