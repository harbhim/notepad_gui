import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QMessageBox, QFontDialog, QColorDialog, QFileDialog, QInputDialog
from PyQt6.QtGui import QAction, QTextCursor, QColor, QFont
from PyQt6.QtCore import Qt

class Notepad(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        self.ui()

        self.show()

    def ui(self):

        self.setMinimumSize(1000,600)
        self.setWindowTitle('Rich Text Notepad GUI')

        self.mainWindowSetup()
        self.createActions()
        self.createMenuItems()

    def mainWindowSetup(self):

        self.menu_bar = self.menuBar()
        self.te = QTextEdit()
        self.te.textChanged.connect(self.removeHighlight)
        self.setCentralWidget(self.te)

    def createActions(self):

        self.open_file = QAction('&Open')
        self.open_file.setShortcut('Ctrl+O')
        self.open_file.triggered.connect(self.openFile)

        self.new_file = QAction('&New')
        self.new_file.setShortcut('Ctrl+N')
        self.new_file.triggered.connect(self.newFile)

        self.save_file = QAction('&Save')
        self.save_file.setShortcut('Ctrl+S')
        self.save_file.triggered.connect(self.saveFile)

        self.quit_file = QAction('&Quit')
        self.quit_file.setShortcut('Ctrl+Q')
        self.quit_file.triggered.connect(self.close)

        self.undo_edit = QAction('&Undo')
        self.undo_edit.setShortcut('Ctrl+Z')
        self.undo_edit.triggered.connect(self.te.undo)

        self.redo_edit = QAction('&Redo')
        self.redo_edit.setShortcut('Ctrl+Shift+Z')
        self.redo_edit.triggered.connect(self.te.redo)

        self.cut_edit = QAction('&Cut')
        self.cut_edit.setShortcut('Ctrl+X')
        self.cut_edit.triggered.connect(self.te.cut)

        self.copy_edit = QAction('&Copy')
        self.copy_edit.setShortcut('Ctrl+C')
        self.copy_edit.triggered.connect(self.te.copy)

        self.paste_edit = QAction('&Paste')
        self.paste_edit.setShortcut('Ctrl+V')
        self.paste_edit.triggered.connect(self.te.paste)

        self.find_edit = QAction('&Find All')
        self.find_edit.setShortcut('Ctrl+F')
        self.find_edit.triggered.connect(self.findText)

        self.font_tool = QAction('&Font')
        self.font_tool.setShortcut('Ctrl+T')
        self.font_tool.triggered.connect(self.selectFont)

        self.font_color = QAction('&Font Color')
        self.font_color.setShortcut('Ctrl+Shift+T')
        self.font_color.triggered.connect(self.selectFontColor)

        self.font_hl = QAction('&Font Hi-light')
        self.font_hl.setShortcut('Ctrl+H')
        self.font_hl.triggered.connect(self.selectFontHL)

        self.about_help = QAction('&About')
        self.about_help.setShortcut('Ctrl+Shift+H')
        self.about_help.triggered.connect(self.aboutDialog)

    def createMenuItems(self):

        self.file_menu = self.menu_bar.addMenu('&File')
        self.file_menu.addAction(self.new_file)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.open_file)
        self.file_menu.addAction(self.save_file)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.quit_file)

        self.edit_menu = self.menu_bar.addMenu('&Edit')
        self.edit_menu.addAction(self.undo_edit)
        self.edit_menu.addAction(self.redo_edit)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.cut_edit)
        self.edit_menu.addAction(self.copy_edit)
        self.edit_menu.addAction(self.paste_edit)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.find_edit)

        self.tools_menu = self.menu_bar.addMenu('&Tools')
        self.tools_menu.addAction(self.font_tool)
        self.tools_menu.addAction(self.font_color)
        self.tools_menu.addAction(self.font_hl)

        self.help_menu = self.menu_bar.addMenu('&Help')
        self.help_menu.addAction(self.about_help)

    def openFile(self):

        of = QFileDialog.getOpenFileName(self, 'Open File', '/home/study/', 'All Files (*);; Text File (*.txt)')
        with open(of[0],'r') as f:
            notepad_text = f.read()
        self.te.setText(notepad_text)

    def newFile(self):

        mb = QMessageBox.question(self, 'Create New File', 'Are you sure want to create new file?', QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Cancel)

        if mb == QMessageBox.StandardButton.Ok:
            self.te.clear()

    def saveFile(self):

        fd = QFileDialog.getSaveFileName(self, 'Save File Dialog', '/home/study/', 'Text File (*.txt);;Python File (*.py)')

        if fd[0].endswith(('txt', 'py')):
            text = self.te.toPlainText()
            with open(fd[0], 'w') as fs:
                fs.write(text)

        elif fd[0].endswith('html'):
            text = self.te.toHtml()
            with open(fd[0], 'w') as fs:
                fs.write(text)

        else:
            mb = QMessageBox.information(self, 'Not Saved', 'Extension not Found', QMessageBox.StandardButton.Ok)

    def findText(self):

        find_text = QInputDialog.getText(self, 'Search Text', 'Find : ')

        if find_text[1]:

            extra_selection = []

            self.te.moveCursor(QTextCursor.MoveOperation.Start)
            color = QColor(Qt.GlobalColor.gray)
            while self.te.find(find_text[0]):
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(color)
                selection.cursor = self.te.textCursor()
                extra_selection.append(selection)
                self.te.setExtraSelections(extra_selection)

    def removeHighlight(self):

        self.te.setExtraSelections([])

    def selectFont(self):

        cur = self.te.currentFont()
        options = QFontDialog.FontDialogOption.DontUseNativeDialog
        font = QFontDialog.getFont(cur, self, options=options)
        if font[1]:
            self.te.setCurrentFont(font[0])

    def selectFontColor(self):

        color = QColorDialog.getColor()
        self.te.setTextColor(color)

    def selectFontHL(self):

        color = QColorDialog.getColor()
        self.te.setTextBackgroundColor(color)

    def aboutDialog(self):

        ad = QMessageBox.about(self, 'About Data', 'Created by Hardik Bhimani')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Notepad()
    sys.exit(app.exec())
