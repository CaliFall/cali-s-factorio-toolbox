import sys

import winsound

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QFontMetrics, QMovie

from toolbox_ui.ui_main import Ui_MainWindow
from toolbox_ui.dialog_text_edit import Ui_DialogTextEdit
from my_factorio_funcs import *
from my_factorio_lib import Blueprint


class DialogTextEdit(QDialog):
	"""用于编辑长文本的对话框"""
	
	def __init__(self, parent=None, raw_text: str = ''):
		super().__init__(parent)
		
		self.ui = Ui_DialogTextEdit()
		self.ui.setupUi(self)
		
		self.ui.plainTextEdit_content.setPlainText(raw_text)
		self.ui.pushButton_confirm.clicked.connect(self.confirm)
		self.ui.pushButton_cancel.clicked.connect(self.cancel)
	
	def confirm(self):
		self.returned_text = self.ui.plainTextEdit_content.toPlainText()
		super().accept()
	
	def cancel(self):
		super().close()


class MainWindow(QMainWindow):
	def __init__(self):
		__version__ = '0.0.2'
		
		super(MainWindow, self).__init__()
		
		# 使用生成的UI文件创建UI
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)  # 禁用最大化按钮
		self.setWindowTitle("Cali's Factorio Toolbox" + " Ver" + __version__)  # 设置软件标题
		
		self.setFont(QFont("微软雅黑"))
		self.set_additional_css()  # 设置额外的css
		self.init_signals()  # 初始化信号
		
		# 变量
		self.mini_image_file_path: str = ''  # 静态小图片生成功能中加载的图片地址
		self.mini_image_dynamic_file_path: str = ''  # 动态小图片生成功能中加载的图片地址
		self.__blueprint_loaded_bp: Blueprint | None = None  # 蓝图编辑功能中加载的蓝图对象
	
	def set_additional_css(self) -> None:
		"""设置额外的css"""
		additional_css = ''
		
		# additional_css += """
		# 	QMainWindow{
		# 		background-color: black;
		# 	}
		# """
		
		self.setStyleSheet(self.styleSheet() + additional_css)
	
	def init_signals(self) -> None:
		"""初始化信号"""
		# 显示屏
		self.ui.pushButton_mini_screen_generate.clicked.connect(self.on_mini_screen_generate_clicked)
		self.ui.pushButton_mini_screen_copy.clicked.connect(self.on_mini_screen_copy_clicked)
		# 静态小图片
		self.ui.pushButton_mini_image_select.clicked.connect(self.on_mini_image_select_clicked)
		self.ui.pushButton_mini_image_generate.clicked.connect(self.on_mini_image_generate_clicked)
		self.ui.pushButton_mini_image_copy.clicked.connect(self.on_mini_image_copy_clicked)
		# 动态小图片
		self.ui.pushButton_mini_image_dynamic_select.clicked.connect(self.on_mini_image_dynamic_select_clicked)
		self.ui.pushButton_mini_image_dynamic_generate.clicked.connect(self.on_mini_image_dynamic_generate_clicked)
		self.ui.pushButton_mini_image_dynamic_copy.clicked.connect(self.on_mini_image_dynamic_copy_clicked)
		# 蓝图
		self.ui.pushButton_blueprint_clear.clicked.connect(self.on_blueprint_clear_clicked)
		self.ui.pushButton_blueprint_analyze.clicked.connect(self.on_blueprint_analyze_clicked)
		self.ui.pushButton_blueprint_label_edit.clicked.connect(self.on_blueprint_label_edit_clicked)
		self.ui.pushButton_blueprint_description_edit.clicked.connect(self.on_blueprint_description_edit_clicked)
		self.ui.pushButton_blueprint_copy.clicked.connect(self.on_blueprint_copy_clicked)
	
	"""显示屏生成相关"""
	
	def on_mini_screen_generate_clicked(self) -> None:
		"""生成显示屏蓝图按钮按下时触发"""
		
		# 检查像素总数是否合法
		pix_count = self.ui.spinBox_mini_screen_width.value() * self.ui.spinBox_mini_screen_height.value()
		if pix_count <= 0 or pix_count > 2935:
			QMessageBox.critical(self, "错误", "请确保像素数量在1~2935之间", QMessageBox.Ok)
			return
		
		# 将结果输出到右侧textEdit中
		wires_type_list = []
		if self.ui.checkBox_mini_screen_red_wire.checkState():
			wires_type_list.append(1)
		if self.ui.checkBox_mini_screen_green_wire.checkState():
			wires_type_list.append(2)
		
		bp = generate_screen_blueprint(
			self.ui.spinBox_mini_screen_width.value(),
			self.ui.spinBox_mini_screen_height.value(),
			wires_type_list,
			bool(self.ui.checkBox_mini_screen_always_on.checkState())
		)
		
		self.ui.plainTextEdit_mini_screen_output.setPlainText(bp)
	
	def on_mini_screen_copy_clicked(self) -> None:
		"""复制显示屏蓝图按钮按下时触发"""
		
		pyperclip.copy(self.ui.plainTextEdit_mini_screen_output.toPlainText())
		winsound.MessageBeep()
	
	"""静态小图片蓝图生成相关"""
	
	def on_mini_image_select_clicked(self) -> None:
		"""选择静态小图片按钮按下时触发"""
		
		file_path, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "", "Image Files (*.jpg *.jpeg *.png)")
		if file_path:
			self.mini_image_file_path = file_path
			print(file_path)
			
			# 在label中预览图片
			self.ui.label_mini_image.setPixmap(QPixmap(file_path))
			self.ui.label_mini_image.setScaledContents(True)
	
	def on_mini_image_generate_clicked(self) -> None:
		"""生成静态小图片蓝图按钮按下时触发"""
		
		if not self.mini_image_file_path:
			QMessageBox.critical(self, "错误", "尚未选择图片", QMessageBox.Ok)
			return
		
		pix_count = self.ui.spinBox_mini_image_width.value() * self.ui.spinBox_mini_image_height.value()
		if pix_count <= 0 or pix_count > 2935:
			QMessageBox.critical(self, "错误", "请确保像素数量在1~2935之间", QMessageBox.Ok)
			return
		
		self.ui.plainTextEdit_mini_image_output.setPlainText(
			generate_mini_static_image_blueprint(
				self.mini_image_file_path,
				self.ui.spinBox_mini_image_width.value(),
				self.ui.spinBox_mini_image_height.value()
			)
		)
	
	def on_mini_image_copy_clicked(self) -> None:
		"""复制小静态图片蓝图按钮按下时触发"""
		
		pyperclip.copy(self.ui.plainTextEdit_mini_image_output.toPlainText())
		winsound.MessageBeep()
	
	"""动态小图片蓝图生成相关"""
	
	def on_mini_image_dynamic_select_clicked(self) -> None:
		"""选择动态小图片按钮按下时触发"""
		
		file_path, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "", "Image Files (*.gif)")
		if file_path:
			self.mini_image_dynamic_file_path = file_path
			print(file_path)
			
			# 在label中预览图片
			movie = QMovie(file_path)
			self.ui.label_mini_image_dynamic.setMovie(movie)
			movie.setScaledSize(self.ui.label_mini_image_dynamic.size())
			movie.start()
			
			# 同步帧间间隔到ui
			self.ui.spinBox_mini_image_dynamic_duration.setValue(get_gif_duration(file_path))
	
	def on_mini_image_dynamic_generate_clicked(self) -> None:
		"""生成动态小图片蓝图按钮按下时触发"""
		
		if not self.mini_image_dynamic_file_path:
			QMessageBox.critical(self, "错误", "尚未选择图片", QMessageBox.Ok)
			return
		
		pix_count = self.ui.spinBox_mini_image_dynamic_width.value() * self.ui.spinBox_mini_image_dynamic_height.value()
		if pix_count <= 0 or pix_count > 2935:
			QMessageBox.critical(self, "错误", "请确保像素数量在1~2935之间", QMessageBox.Ok)
			return
		
		self.ui.plainTextEdit_mini_image_dynamic_output.setPlainText(
			generate_mini_dynamic_image_blueprint(
				self.mini_image_dynamic_file_path,
				self.ui.spinBox_mini_image_dynamic_width.value(),
				self.ui.spinBox_mini_image_dynamic_height.value(),
				self.ui.spinBox_mini_image_dynamic_duration.value()
			)
		)
	
	def on_mini_image_dynamic_copy_clicked(self) -> None:
		"""复制小动态图片按钮按下时触发"""
		
		pyperclip.copy(self.ui.plainTextEdit_mini_image_dynamic_output.toPlainText())
		winsound.MessageBeep()
	
	"""蓝图编辑功能相关"""
	
	def refresh_blueprint_controls(self) -> None:
		"""加载的蓝图对象变动时触发"""
		
		# 更新控件
		metrics = QFontMetrics(self.ui.label_blueprint_label.font())
		self.ui.label_blueprint_label.setText(
			metrics.elidedText(self.blueprint_loaded_bp.label, Qt.ElideRight, 200))
		self.ui.label_blueprint_description.setText(
			metrics.elidedText(self.blueprint_loaded_bp.description, Qt.ElideRight, 200))
		
		for icon in self.blueprint_loaded_bp.icons:
			match icon.index:
				case 1:
					self.ui.label_blueprint_icon_1.setText(icon.signal['name'])
				case 2:
					self.ui.label_blueprint_icon_2.setText(icon.signal['name'])
				case 3:
					self.ui.label_blueprint_icon_3.setText(icon.signal['name'])
				case 4:
					self.ui.label_blueprint_icon_4.setText(icon.signal['name'])
	
	def on_blueprint_clear_clicked(self) -> None:
		"""清空按钮"""
		
		self.ui.plainTextEdit_blueprint_input.setPlainText('')
	
	def on_blueprint_analyze_clicked(self) -> None:
		"""分析按钮"""
		
		# 尝试将代码转换为字典
		try:
			bp_dict = blueprint_to_dict(self.ui.plainTextEdit_blueprint_input.toPlainText())
		except Exception as e:
			QMessageBox.critical(self, '错误', str(e), QMessageBox.Ok)
			return
		
		# 判断是否是合法的蓝图代码
		if 'blueprint' not in bp_dict:
			QMessageBox.critical(self, '错误', '代码中未查找到蓝图字典', QMessageBox.Ok)
			return
		
		# 尝试对象化
		try:
			self.blueprint_loaded_bp = Blueprint(bp_dict)
		except Exception as e:
			QMessageBox.critical(self, '错误', str(e), QMessageBox.Ok)
			return
		
		# 刷新控件
		self.refresh_blueprint_controls()
		
		# 解锁编辑按钮
		self.ui.pushButton_blueprint_label_edit.setEnabled(True)
		self.ui.pushButton_blueprint_description_edit.setEnabled(True)
		self.ui.pushButton_blueprint_icon_1_edit.setEnabled(True)
		self.ui.pushButton_blueprint_icon_2_edit.setEnabled(True)
		self.ui.pushButton_blueprint_icon_3_edit.setEnabled(True)
		self.ui.pushButton_blueprint_icon_4_edit.setEnabled(True)
	
	def on_blueprint_label_edit_clicked(self) -> None:
		"""编辑蓝图名称按钮"""
		dialog = DialogTextEdit(self, self.ui.label_blueprint_label.text())
		if dialog.exec_() == QDialog.Accepted:
			self.blueprint_loaded_bp.label = dialog.returned_text
			self.refresh_blueprint_controls()
	
	def on_blueprint_description_edit_clicked(self) -> None:
		"""编辑蓝图简介按钮"""
		dialog = DialogTextEdit(self, self.ui.label_blueprint_label.text())
		if dialog.exec_() == QDialog.Accepted:
			self.blueprint_loaded_bp.description = dialog.returned_text
			self.refresh_blueprint_controls()
	
	def on_blueprint_copy_clicked(self) -> None:
		"""复制蓝图按钮"""
		pyperclip.copy(dict_to_blueprint(self.blueprint_loaded_bp.get_dict()))


if __name__ == '__main__':
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 启用HD缩放
	
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	sys.exit(app.exec_())
