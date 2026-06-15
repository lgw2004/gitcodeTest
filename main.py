"""
PySide6 桌面开发 Demo
=====================
展示 PySide6 的核心概念：
- QMainWindow 主窗口框架 (菜单栏、工具栏、状态栏)
- 布局管理 (QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout)
- 常用控件 (按钮、标签、输入框、下拉框、进度条、表格、树形控件等)
- 信号与槽 (Signal & Slot) 事件机制
- 对话框 (QMessageBox, QFileDialog, QInputDialog)
- 多标签页 (QTabWidget)
- 样式表 (QSS) 美化
"""

import sys
import random
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout, QGroupBox,
    QLabel, QPushButton, QLineEdit, QTextEdit, QPlainTextEdit,
    QComboBox, QSpinBox, QSlider, QProgressBar, QCheckBox, QRadioButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTreeWidget, QTreeWidgetItem,
    QListWidget, QListWidgetItem, QTabWidget,
    QMenuBar, QMenu, QToolBar, QStatusBar,
    QMessageBox, QFileDialog, QInputDialog, QFontDialog, QColorDialog,
    QDialog, QDialogButtonBox, QFrame, QSplitter,
    QButtonGroup, QScrollArea, QSizePolicy, QSpacerItem,
)
from PySide6.QtCore import Qt, QTimer, QSize, QSettings
from PySide6.QtGui import QAction, QIcon, QFont, QColor, QPalette

# =============================================================================
# 自定义对话框 - 演示 QDialog
# =============================================================================
class AboutDialog(QDialog):
    """关于对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于")
        self.setFixedSize(360, 200)

        layout = QVBoxLayout(self)

        title = QLabel("PySide6 Demo 应用")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")

        info = QLabel("这是一个 PySide6 桌面开发的演示程序。\n"
                      "展示了常用控件、布局、信号与槽等核心概念。")
        info.setAlignment(Qt.AlignCenter)
        info.setWordWrap(True)

        btn = QDialogButtonBox(QDialogButtonBox.Ok)
        btn.accepted.connect(self.accept)

        layout.addWidget(title)
        layout.addWidget(info)
        layout.addWidget(btn)


# =============================================================================
# Tab 1: 基础控件展示
# =============================================================================
class BasicWidgetsTab(QWidget):
    """基础控件标签页"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # --- 按钮组 ---
        btn_group = QGroupBox("按钮 (QPushButton)")
        btn_layout = QVBoxLayout(btn_group)

        row1 = QHBoxLayout()
        self.normal_btn = QPushButton("普通按钮")
        self.toggle_btn = QPushButton("可切换按钮")
        self.toggle_btn.setCheckable(True)
        self.flat_btn = QPushButton("扁平按钮")
        self.flat_btn.setFlat(True)
        row1.addWidget(self.normal_btn)
        row1.addWidget(self.toggle_btn)
        row1.addWidget(self.flat_btn)

        btn_status = QLabel("按钮状态：等待点击...")
        btn_layout.addLayout(row1)
        btn_layout.addWidget(btn_status)

        # 信号连接
        self.normal_btn.clicked.connect(lambda: btn_status.setText("普通按钮被点击！"))
        self.toggle_btn.toggled.connect(lambda checked: btn_status.setText(
            f"切换按钮：{'按下' if checked else '弹起'}"))
        self.flat_btn.clicked.connect(lambda: btn_status.setText("扁平按钮被点击！"))

        # --- 输入控件组 ---
        input_group = QGroupBox("输入控件")
        input_layout = QFormLayout(input_group)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("请输入文本...")
        self.line_edit.setClearButtonEnabled(True)

        self.combo = QComboBox()
        self.combo.addItems(["选项 1", "选项 2", "选项 3", "选项 4"])
        self.combo.setCurrentIndex(0)

        self.spin = QSpinBox()
        self.spin.setRange(0, 100)
        self.spin.setValue(50)
        self.spin.setSuffix(" %")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)

        input_layout.addRow("文本输入：", self.line_edit)
        input_layout.addRow("下拉选择：", self.combo)
        input_layout.addRow("数字输入：", self.spin)
        input_layout.addRow("滑动条：", self.slider)

        # --- 选择控件组 ---
        check_group = QGroupBox("选择控件")
        check_layout = QVBoxLayout(check_group)

        self.check1 = QCheckBox("启用功能 A")
        self.check2 = QCheckBox("启用功能 B")
        self.check3 = QCheckBox("启用功能 C (三态)", self)
        self.check3.setTristate(True)
        self.check1.setChecked(True)

        radio_group = QButtonGroup(self)
        radio_layout_h = QHBoxLayout()
        self.radio1 = QRadioButton("模式 A")
        self.radio2 = QRadioButton("模式 B")
        self.radio3 = QRadioButton("模式 C")
        self.radio1.setChecked(True)
        radio_group.addButton(self.radio1)
        radio_group.addButton(self.radio2)
        radio_group.addButton(self.radio3)
        radio_layout_h.addWidget(self.radio1)
        radio_layout_h.addWidget(self.radio2)
        radio_layout_h.addWidget(self.radio3)
        radio_layout_h.addStretch()

        check_layout.addWidget(self.check1)
        check_layout.addWidget(self.check2)
        check_layout.addWidget(self.check3)
        check_layout.addLayout(radio_layout_h)

        # --- 进度与状态组 ---
        progress_group = QGroupBox("进度与状态")
        progress_layout = QVBoxLayout(progress_group)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("开始进度")
        self.reset_btn = QPushButton("重置")
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.reset_btn)
        btn_row.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick_progress)
        self._progress_value = 0

        self.start_btn.clicked.connect(self._toggle_progress)
        self.reset_btn.clicked.connect(self._reset_progress)

        progress_layout.addWidget(self.progress_bar)
        progress_layout.addLayout(btn_row)

        # 添加到主布局
        layout.addWidget(btn_group)
        layout.addWidget(input_group)
        layout.addWidget(check_group)
        layout.addWidget(progress_group)
        layout.addStretch()

    def _toggle_progress(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText("继续进度")
        else:
            if self._progress_value >= 100:
                self._progress_value = 0
            self.timer.start(50)
            self.start_btn.setText("暂停进度")

    def _tick_progress(self):
        self._progress_value += 1
        self.progress_bar.setValue(self._progress_value)
        if self._progress_value >= 100:
            self.timer.stop()
            self.start_btn.setText("开始进度")

    def _reset_progress(self):
        self.timer.stop()
        self._progress_value = 0
        self.progress_bar.setValue(0)
        self.start_btn.setText("开始进度")


# =============================================================================
# Tab 2: 高级控件
# =============================================================================
class AdvancedWidgetsTab(QWidget):
    """高级控件标签页"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # --- 表格控件 ---
        table_group = QGroupBox("表格控件 (QTableWidget)")
        table_layout = QVBoxLayout(table_group)

        self.table = QTableWidget(4, 4)
        self.table.setHorizontalHeaderLabels(["姓名", "年龄", "城市", "职业"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)

        # 填充示例数据
        sample_data = [
            ["张三", "28", "北京", "工程师"],
            ["李四", "32", "上海", "设计师"],
            ["王五", "25", "广州", "产品经理"],
            ["赵六", "30", "深圳", "数据分析师"],
        ]
        for row, data in enumerate(sample_data):
            for col, text in enumerate(data):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

        btn_row = QHBoxLayout()
        add_row_btn = QPushButton("添加行")
        del_row_btn = QPushButton("删除选中行")
        add_row_btn.clicked.connect(self._add_table_row)
        del_row_btn.clicked.connect(self._del_table_row)
        btn_row.addWidget(add_row_btn)
        btn_row.addWidget(del_row_btn)
        btn_row.addStretch()

        table_layout.addWidget(self.table)
        table_layout.addLayout(btn_row)

        # --- 树形控件 ---
        tree_group = QGroupBox("树形控件 (QTreeWidget)")
        tree_layout = QVBoxLayout(tree_group)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["项目", "说明"])

        # 根节点
        animals = QTreeWidgetItem(self.tree, ["动物", "各种动物"])
        cat = QTreeWidgetItem(animals, ["猫科", "猫科动物"])
        QTreeWidgetItem(cat, ["猫", "喵星人"])
        QTreeWidgetItem(cat, ["狮子", "草原之王"])
        dog = QTreeWidgetItem(animals, ["犬科", "犬科动物"])
        QTreeWidgetItem(dog, ["狗", "汪星人"])
        QTreeWidgetItem(dog, ["狼", "森林猎手"])

        plants = QTreeWidgetItem(self.tree, ["植物", "各种植物"])
        trees = QTreeWidgetItem(plants, ["树木", "木本植物"])
        QTreeWidgetItem(trees, ["松树", "常绿乔木"])
        QTreeWidgetItem(trees, ["柳树", "落叶乔木"])

        self.tree.expandAll()
        self.tree.itemClicked.connect(
            lambda item, col: self._status_label.setText(
                f"选中了: {item.text(0)} - {item.text(1)}"))

        self._status_label = QLabel("点击树形控件中的项目...")

        tree_layout.addWidget(self.tree)
        tree_layout.addWidget(self._status_label)

        # --- 文本编辑 ---
        text_group = QGroupBox("文本编辑 (QTextEdit)")
        text_layout = QVBoxLayout(text_group)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("这里是一个富文本编辑器...\n支持多行文本、粘贴等操作。")
        self.text_edit.setMaximumHeight(100)

        info_label = QLabel()
        self.text_edit.textChanged.connect(
            lambda: info_label.setText(f"字符数：{len(self.text_edit.toPlainText())}"))

        text_layout.addWidget(self.text_edit)
        text_layout.addWidget(info_label)

        layout.addWidget(table_group)
        layout.addWidget(tree_group)
        layout.addWidget(text_group)

    def _add_table_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col in range(4):
            self.table.setItem(row, col, QTableWidgetItem(f"新数据 {col+1}"))

    def _del_table_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)


# =============================================================================
# Tab 3: 布局演示
# =============================================================================
class LayoutDemoTab(QWidget):
    """布局演示标签页"""
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)

        # --- Grid 布局 ---
        grid_group = QGroupBox("网格布局 (QGridLayout) - 计算器面板")
        grid = QGridLayout(grid_group)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', '(', ')', '⌫',
        ]

        self.calc_display = QLineEdit("0")
        self.calc_display.setAlignment(Qt.AlignRight)
        self.calc_display.setReadOnly(True)
        self.calc_display.setStyleSheet("font-size: 20px; padding: 8px;")
        grid.addWidget(self.calc_display, 0, 0, 1, 4)

        positions = [(i // 4 + 1, i % 4) for i in range(20)]
        for pos, text in zip(positions, buttons):
            btn = QPushButton(text)
            btn.setMinimumSize(50, 40)
            btn.clicked.connect(lambda checked, t=text: self._calc_click(t))
            grid.addWidget(btn, pos[0], pos[1])

        # --- 水平/垂直布局 ---
        hz_group = QGroupBox("水平与垂直布局")
        hz_main = QVBoxLayout(hz_group)

        # 水平
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("水平布局 →"))
        for i in range(4):
            btn = QPushButton(f"按钮{i+1}")
            hbox.addWidget(btn)
        hbox.addStretch()
        hz_main.addLayout(hbox)

        # 分隔线
        hz_main.addWidget(_make_separator())

        # 垂直
        inner_hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("↓ 垂直布局"))
        for i in range(3):
            btn = QPushButton(f"项目 {i+1}")
            vbox.addWidget(btn)
        vbox.addStretch()
        inner_hbox.addLayout(vbox)
        inner_hbox.addWidget(_make_separator(Qt.Vertical))

        # Form 布局
        form = QFormLayout()
        form.addRow("姓名：", QLineEdit())
        form.addRow("邮箱：", QLineEdit())
        form.addRow("电话：", QLineEdit())
        form.addRow("地址：", QLineEdit())
        inner_hbox.addLayout(form)

        hz_main.addLayout(inner_hbox)

        # --- Splitter 分割面板 ---
        split_group = QGroupBox("分割面板 (QSplitter)")
        split_layout = QVBoxLayout(split_group)
        splitter = QSplitter(Qt.Horizontal)
        left_panel = QTextEdit()
        left_panel.setPlaceholderText("左侧面板 - 可以拖动中间的分割条调整大小")
        right_panel = QTextEdit()
        right_panel.setPlaceholderText("右侧面板 - 可以拖动中间的分割条调整大小")

        # 美化面板
        left_panel.setStyleSheet("background: #f0f4ff;")
        right_panel.setStyleSheet("background: #fff0f0;")

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 300])
        split_layout.addWidget(splitter)

        main_layout.addWidget(grid_group)
        main_layout.addWidget(hz_group)
        main_layout.addWidget(split_group)

    def _calc_click(self, text):
        """简单计算器逻辑"""
        current = self.calc_display.text()
        if text == 'C':
            self.calc_display.setText('0')
        elif text == '⌫':
            self.calc_display.setText(current[:-1] if len(current) > 1 else '0')
        elif text == '=':
            try:
                result = eval(current)
                self.calc_display.setText(str(result))
            except Exception:
                self.calc_display.setText('Error')
        else:
            if current == '0' and text not in '+-*/':
                self.calc_display.setText(text)
            else:
                self.calc_display.setText(current + text)


# =============================================================================
# Tab 4: 信号与槽
# =============================================================================
class SignalSlotTab(QWidget):
    """信号与槽演示标签页"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # 说明
        desc = QLabel(
            "信号与槽 (Signal & Slot) 是 Qt 的核心机制，\n"
            "用于对象之间的通信。当某个事件发生时，\n"
            "发射信号，连接的槽函数会被自动调用。"
        )
        desc.setStyleSheet("font-size: 14px; color: #555; padding: 10px;")
        layout.addWidget(desc)

        # 示例 1: 按钮信号
        ex1 = QGroupBox("示例 1: 按钮点击 → 更新标签")
        ex1_layout = QVBoxLayout(ex1)
        ex1_btn = QPushButton("点击我")
        ex1_label = QLabel("等待...")
        ex1_label.setAlignment(Qt.AlignCenter)
        ex1_btn.clicked.connect(lambda: ex1_label.setText(
            f"按钮被点击了！计数：{random.randint(1, 100)}"))
        ex1_layout.addWidget(ex1_btn)
        ex1_layout.addWidget(ex1_label)

        # 示例 2: 滑块联动
        ex2 = QGroupBox("示例 2: 滑块 ↔ 数字框 双向联动")
        ex2_layout = QHBoxLayout(ex2)
        slider2 = QSlider(Qt.Horizontal)
        spin2 = QSpinBox()
        slider2.setRange(0, 100)
        spin2.setRange(0, 100)
        # 连接两个方向
        slider2.valueChanged.connect(spin2.setValue)
        spin2.valueChanged.connect(slider2.setValue)
        slider2.setValue(42)
        ex2_layout.addWidget(slider2)
        ex2_layout.addWidget(spin2)

        # 示例 3: 文本改变事件
        ex3 = QGroupBox("示例 3: 文本变化 → 实时统计")
        ex3_layout = QVBoxLayout(ex3)
        text_input = QTextEdit()
        text_input.setPlaceholderText("在这里输入文字...")
        stats = QLabel("字数: 0 | 行数: 0 | 字符数: 0")
        text_input.textChanged.connect(
            lambda: stats.setText(
                f"字数: {len(text_input.toPlainText().split())} | "
                f"行数: {text_input.document().lineCount()} | "
                f"字符数: {len(text_input.toPlainText())}"))
        ex3_layout.addWidget(text_input)
        ex3_layout.addWidget(stats)

        # 示例 4: 下拉框变化
        ex4 = QGroupBox("示例 4: 下拉选择 → 动态更新背景色")
        ex4_layout = QHBoxLayout(ex4)
        color_combo = QComboBox()
        color_combo.addItems(["默认", "浅蓝", "浅绿", "浅黄", "浅粉"])
        preview = QFrame()
        preview.setMinimumSize(100, 40)
        preview.setStyleSheet("background: white; border: 1px solid #ccc;")

        color_map = {
            "默认": "#ffffff", "浅蓝": "#dbeafe", "浅绿": "#dcfce7",
            "浅黄": "#fef9c3", "浅粉": "#fce7f3"
        }
        color_combo.currentTextChanged.connect(
            lambda text: preview.setStyleSheet(
                f"background: {color_map.get(text, '#fff')}; "
                f"border: 1px solid #ccc;"))

        ex4_layout.addWidget(QLabel("选择颜色："))
        ex4_layout.addWidget(color_combo)
        ex4_layout.addWidget(preview)
        ex4_layout.addStretch()

        layout.addWidget(ex1)
        layout.addWidget(ex2)
        layout.addWidget(ex3)
        layout.addWidget(ex4)
        layout.addStretch()


# =============================================================================
# 辅助函数
# =============================================================================
def _make_separator(orientation=Qt.Horizontal) -> QFrame:
    """创建一条分隔线"""
    line = QFrame()
    shape = QFrame.HLine if orientation == Qt.Horizontal else QFrame.VLine
    line.setFrameShape(shape)
    line.setFrameShadow(QFrame.Sunken)
    line.setStyleSheet("background: #ddd;")
    return line


# =============================================================================
# 主窗口
# =============================================================================
class MainWindow(QMainWindow):
    """主窗口 - 整合所有 Tab 和菜单"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 桌面开发 Demo")
        self.resize(900, 650)

        # --- 设置应用样式 ---
        self._apply_stylesheet()

        # --- 创建菜单栏 ---
        self._create_menus()

        # --- 创建工具栏 ---
        self._create_toolbar()

        # --- 创建状态栏 ---
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("就绪")

        # --- 创建中央 Tab 控件 ---
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(BasicWidgetsTab(), "基础控件")
        self.tab_widget.addTab(AdvancedWidgetsTab(), "高级控件")
        self.tab_widget.addTab(LayoutDemoTab(), "布局演示")
        self.tab_widget.addTab(SignalSlotTab(), "信号与槽")
        self.tab_widget.currentChanged.connect(
            lambda idx: self.status_bar.showMessage(
                f"当前标签页：{self.tab_widget.tabText(idx)}"))

        self.setCentralWidget(self.tab_widget)

    def _apply_stylesheet(self):
        """全局样式表 (QSS)"""
        self.setStyleSheet("""
            QMainWindow {
                background: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                background: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #1976D2;
            }
            QTabBar::tab:hover:!selected {
                background: #eee;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 6px;
            }
            QPushButton {
                background: #1976D2;
                color: white;
                border: none;
                padding: 6px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #1565C0;
            }
            QPushButton:pressed {
                background: #0D47A1;
            }
            QPushButton:flat {
                background: transparent;
                color: #1976D2;
                border: 1px solid #1976D2;
            }
            QPushButton:flat:hover {
                background: #e3f2fd;
            }
            QLineEdit, QTextEdit, QPlainTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #1976D2;
            }
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
            }
            QSlider::handle:horizontal {
                background: #1976D2;
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: #1976D2;
                border-radius: 3px;
            }
            QTableWidget {
                gridline-color: #ddd;
                border: 1px solid #ccc;
            }
            QHeaderView::section {
                background: #1976D2;
                color: white;
                padding: 4px;
                border: none;
            }
            QTreeWidget {
                border: 1px solid #ccc;
            }
            QMenuBar {
                background: white;
                border-bottom: 1px solid #ddd;
            }
            QMenuBar::item:selected {
                background: #e3f2fd;
            }
            QToolBar {
                background: white;
                border-bottom: 1px solid #ddd;
                spacing: 4px;
            }
            QStatusBar {
                background: white;
                border-top: 1px solid #ddd;
            }
        """)

    def _create_menus(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()

        # --- 文件菜单 ---
        file_menu = menu_bar.addMenu("文件(&F)")

        new_action = QAction("新建(&N)", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(lambda: self.status_bar.showMessage("新建被点击"))
        file_menu.addAction(new_action)

        open_action = QAction("打开(&O)...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        save_action = QAction("保存(&S)", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(lambda: self.status_bar.showMessage("保存被点击"))
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction("退出(&Q)", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # --- 编辑菜单 ---
        edit_menu = menu_bar.addMenu("编辑(&E)")

        undo_action = QAction("撤销(&U)", self)
        undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(undo_action)

        redo_action = QAction("重做(&R)", self)
        redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        pref_action = QAction("首选项...", self)
        pref_action.triggered.connect(lambda: QMessageBox.information(
            self, "首选项", "这里可以打开设置对话框。"))
        edit_menu.addAction(pref_action)

        # --- 帮助菜单 ---
        help_menu = menu_bar.addMenu("帮助(&H)")

        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(lambda: AboutDialog(self).exec())
        help_menu.addAction(about_action)

        about_qt_action = QAction("关于 Qt", self)
        about_qt_action.triggered.connect(QApplication.aboutQt)
        help_menu.addAction(about_qt_action)

    def _create_toolbar(self):
        """创建工具栏"""
        toolbar = self.addToolBar("主工具栏")
        toolbar.setMovable(False)

        # 消息框按钮
        msg_btn = QPushButton("💬 消息框")
        msg_btn.clicked.connect(self._show_message_box)
        toolbar.addWidget(msg_btn)

        toolbar.addSeparator()

        # 文件对话框按钮
        file_btn = QPushButton("📁 打开文件")
        file_btn.clicked.connect(self._open_file)
        toolbar.addWidget(file_btn)

        toolbar.addSeparator()

        # 输入对话框按钮
        input_btn = QPushButton("✏️ 输入框")
        input_btn.clicked.connect(self._show_input_dialog)
        toolbar.addWidget(input_btn)

        toolbar.addSeparator()

        # 颜色对话框
        color_btn = QPushButton("🎨 颜色选择")
        color_btn.clicked.connect(self._show_color_dialog)
        toolbar.addWidget(color_btn)

        toolbar.addSeparator()

        # 字体对话框
        font_btn = QPushButton("🔤 字体选择")
        font_btn.clicked.connect(self._show_font_dialog)
        toolbar.addWidget(font_btn)

    # ===== 槽函数 =====
    def _show_message_box(self):
        """弹出消息对话框"""
        reply = QMessageBox.question(
            self, "确认", "这是一个消息框示例。\n你想要选择什么？",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.status_bar.showMessage("你选择了：是")
        elif reply == QMessageBox.No:
            self.status_bar.showMessage("你选择了：否")
        else:
            self.status_bar.showMessage("你选择了：取消")

    def _open_file(self):
        """打开文件对话框"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", str(Path.home()),
            "所有文件 (*.*);;文本文件 (*.txt);;图片 (*.png *.jpg)")
        if file_path:
            self.status_bar.showMessage(f"已选择文件：{file_path}")

    def _show_input_dialog(self):
        """弹出输入对话框"""
        text, ok = QInputDialog.getText(
            self, "输入对话框", "请输入一些文字：",
            QLineEdit.Normal, "")
        if ok and text:
            QMessageBox.information(self, "你输入了", f"内容是：\n{text}")
            self.status_bar.showMessage(f"输入了：{text}")

    def _show_color_dialog(self):
        """颜色选择对话框"""
        color = QColorDialog.getColor(QColor("#1976D2"), self, "选择颜色")
        if color.isValid():
            self.status_bar.showMessage(
                f"选择的颜色：{color.name()} | RGB({color.red()},{color.green()},{color.blue()})")

    def _show_font_dialog(self):
        """字体选择对话框"""
        ok, font = QFontDialog.getFont(QFont("Microsoft YaHei", 12), self, "选择字体")
        if ok:
            self.status_bar.showMessage(
                f"选择的字体：{font.family()}, {font.pointSize()}pt")


# =============================================================================
# 程序入口
# =============================================================================
if __name__ == "__main__":
    # 启用高 DPI 缩放（Windows）
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setApplicationName("PySide6 Demo")
    app.setOrganizationName("DemoOrg")

    # 让字体渲染更清晰
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
