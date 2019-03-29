#coding:utf-8
# 导入必须模块
import sys
from PySide.QtCore import Qt
from PySide.QtGui import QApplication, QLabel

# 主函数
if __name__ == '__main__':
    # 创建main application
    myApp = QApplication(sys.argv)
    # 创建Label并设置它的属性
    appLabel = QLabel()
    appLabel.setText("Hello, World!!!\n Look at my first app using PySide")
    appLabel.setAlignment(Qt.AlignCenter)
    appLabel.setWindowTitle("My First Application")
    appLabel.setGeometry(300, 300, 250, 175)
    # 显示这个Label
    appLabel.show()
    # 运行main application
    myApp.exec_()
    sys.exit()