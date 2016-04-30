from PyQt4.QtGui import QApplication, QFont
import sys
from spyderlib.widgets.sourcecode.codeeditor import CodeEditor

app = QApplication(sys.argv)
editor = CodeEditor()
editor.setup_editor(language = "python",font = QFont("Courier New"))
editor.set_text(open(__file__).read()) 
editor.show()
sys.exit(app.exec_())