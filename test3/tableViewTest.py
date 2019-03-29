from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from dbOption import Dao
import sys

class MyList(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.dao = Dao()
        self.container = QVBoxLayout()

        inputContainer = QVBoxLayout()


        layout_id = QHBoxLayout()
        lab_id = QLabel('编号')
        self.textView_id = QLineEdit()
        layout_id.addWidget(lab_id)
        layout_id.addWidget(self.textView_id)

        layout_name = QHBoxLayout()
        lab_name = QLabel('名字')
        self.textView_name = QLineEdit()
        layout_name.addWidget(lab_name)
        layout_name.addWidget(self.textView_name)

        layout_pwd = QHBoxLayout()
        lab_pwd = QLabel('密码')
        self.textView_pwd = QLineEdit()
        layout_pwd.addWidget(lab_pwd)
        layout_pwd.addWidget(self.textView_pwd)


        layout_age = QHBoxLayout()
        lab_age = QLabel('年龄')
        self.textView_age = QLineEdit()
        layout_age.addWidget(lab_age)
        layout_age.addWidget(self.textView_age)


        inputContainer.addLayout(layout_id)
        inputContainer.addLayout(layout_name)
        inputContainer.addLayout(layout_pwd)
        inputContainer.addLayout(layout_age)

        button = QPushButton('提交')
        button.clicked.connect(self.btnClick())
        inputContainer.addWidget(button)


        self.container.addLayout(inputContainer)

        self.tablView =  QListView()
        self.container.addWidget(self.tablView)


        self.setLayout(self.container)
        self.loadData()
    def btnClick(self):
        dic = {'id':self.textView_id, 'name':self.textView_name, 'pwd':self.textView_pwd, 'age':self.textView_age}
        print(dic)
        self.dao.insertPerson(dic)

    def loadData(self):

        dataArr = self.dao.selectAllData()

        myTableViewModel = QStandardItemModel(self.tablView)

        for itemData in dataArr:
            str = "id:%s name:%s psw:%s age:%s " % (itemData['id'], itemData['name'], itemData['pwd'], itemData['age'])
            item = QStandardItem(str)
            myTableViewModel.appendRow(item)

        self.tablView.setModel(myTableViewModel)


    def run(self):
        self.show()


if __name__ == '__main__':
    app = QApplication()
    list = MyList()
    list.run()
    sys.exit(app.exec_())