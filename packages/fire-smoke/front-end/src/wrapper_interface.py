from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import ScrollArea, TitleLabel, CaptionLabel, PushButton, FluentIcon, ToolButton, ToolTipFilter, \
    toggleTheme
from qfluentwidgets.components.date_time.picker_base import SeparatorWidget

from style_sheet import StyleSheet

class ToolBar(QWidget):
    """ Tool bar """

    def __init__(self, title, subtitle, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = TitleLabel(title, self)
        self.subtitleLabel = CaptionLabel(subtitle, self)

        self.documentButton = PushButton(
            self.tr('Documentation'), self, FluentIcon.DOCUMENT)
        self.sourceButton = PushButton(self.tr('Source'), self, FluentIcon.GITHUB)
        self.themeButton = ToolButton(FluentIcon.CONSTRACT, self)
        self.separator = SeparatorWidget(self)
        self.supportButton = ToolButton(FluentIcon.HEART, self)
        self.feedbackButton = ToolButton(FluentIcon.FEEDBACK, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()

        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(138)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 22, 36, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addWidget(self.subtitleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addLayout(self.buttonLayout, 1)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.buttonLayout.setSpacing(4)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.addWidget(self.documentButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.sourceButton, 0, Qt.AlignLeft)
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.themeButton, 0, Qt.AlignRight)
        self.buttonLayout.addWidget(self.separator, 0, Qt.AlignRight)
        self.buttonLayout.addWidget(self.supportButton, 0, Qt.AlignRight)
        self.buttonLayout.addWidget(self.feedbackButton, 0, Qt.AlignRight)
        self.buttonLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.themeButton.installEventFilter(ToolTipFilter(self.themeButton))
        self.supportButton.installEventFilter(ToolTipFilter(self.supportButton))
        self.feedbackButton.installEventFilter(
            ToolTipFilter(self.feedbackButton))
        self.themeButton.setToolTip(self.tr('Toggle theme'))
        self.supportButton.setToolTip(self.tr('Support me'))
        self.feedbackButton.setToolTip(self.tr('Send feedback'))

        # self.themeButton.clicked.connect(lambda: toggleTheme(True))
        # self.supportButton.clicked.connect(signalBus.supportSignal)
        # self.documentButton.clicked.connect(
        #     lambda: QDesktopServices.openUrl(QUrl(HELP_URL)))
        # self.sourceButton.clicked.connect(
        #     lambda: QDesktopServices.openUrl(QUrl(EXAMPLE_URL)))
        # self.feedbackButton.clicked.connect(
        #     lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
        #
        # self.subtitleLabel.setTextColor(QColor(96, 96, 96), QColor(216, 216, 216))


class WrapperInterface(ScrollArea):
    def __init__(self, title: str, subtitle='', parent=None):
        super().__init__(parent=parent)

        self.titleLabel = TitleLabel(title, self)
        self.subtitleLabel = CaptionLabel(subtitle, self)


        self.view = QWidget(self)
        self.setStyleSheet("QWidget{background: transparent}")
        self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 10, 0, 0)

        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)

        self.view.setObjectName('view')

        self.setStyleSheet("QScrollArea{background: transparent; border: none}")
