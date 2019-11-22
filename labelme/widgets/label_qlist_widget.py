from qtpy import QtWidgets


class LabelQListWidget(QtWidgets.QListWidget):

    def __init__(self, *args, **kwargs):
        super(LabelQListWidget, self).__init__(*args, **kwargs)
        self.canvas = None
        self.itemsToShapes = []
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    def __str__(self):
        labels = []
        for (item, shape) in self.itemsToShapes:
            labels.append(item.text())
        return str(labels)

    def get_shape_from_item(self, item):
        for index, (item_, shape) in enumerate(self.itemsToShapes):
            if item_ is item:
                return shape
        return False

    def get_item_from_shape(self, shape):
        for index, (item, shape_) in enumerate(self.itemsToShapes):
            if shape_ is shape:
                return item
        return None

    def get_item_from_label(self, label):
        for index, (item, shape_) in enumerate(self.itemsToShapes):
            if item.text() == label:
                return item

    def get_item_shape_from_label(self, label):
        item = self.get_item_from_label(label)
        shape = self.get_shape_from_item(item)
        return (item, shape)

    def search_for_shape(self, shape):
        # search for shape with equivalent properties
        for index, (item, shape_) in enumerate(self.itemsToShapes):
            if shape.label == shape_.label and shape.points == shape_.points:
                return shape_
        return None

    def clear(self):
        super(LabelQListWidget, self).clear()
        self.itemsToShapes = []

    def setParent(self, parent):
        self.parent = parent

    def dropEvent(self, event):
        shapes = self.shapes
        super(LabelQListWidget, self).dropEvent(event)
        if self.shapes == shapes:
            return
        if self.canvas is None:
            raise RuntimeError('self.canvas must be set beforehand.')
        self.parent.setDirty()
        self.canvas.loadShapes(self.shapes)

    @property
    def shapes(self):
        shapes = []
        for i in range(self.count()):
            item = self.item(i)
            shape = self.get_shape_from_item(item)
            shapes.append(shape)
        return shapes
