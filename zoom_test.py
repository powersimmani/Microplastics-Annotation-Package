#https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
#pyinstaller --onefile pythonScriptName.py
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QMainWindow,QMessageBox,QInputDialog,QAction
import code
import qimage2ndarray
import numpy as np
from ImageJ import MP_VAT,MP_VAT_2,MP_ACT,custom_thresholding,add_grid
from PIL import Image
from UNet_prediction import UNet,parameter_tuning


class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint) #기존에 하던일은 다 하고 좌표정보만 훅하는 객체 
    rubberBandCheck = QtCore.pyqtSignal(QtCore.QPoint)
    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self.save_factor = [1,1]
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        #self.on_screen = None
        self.ori_image = None
        self.mask_image = None
        self.merged_image = None
        self.labeled_image = None
        self.merge_alpha = 0.5
        self.mouse_button = 0
        self.len_start_pos = None
        self.micrometer_per_pix = 1
        self.brush_size = 1 
        self.brush_levels = [
            [[0,0]],
            [[0,0],[-1,0],[1,0],[0,1],[0,-1]],
            [[0,0],[-1,0],[1,0],[0,1],[0,-1],[-1,-1],[-1,1],[1,-1],[1,1]],
            [[0,0],[-1,0],[1,0],[0,1],[0,-1],[-1,-1],[-1,1],[1,-1],[1,1],[-2,0],[2,0],[0,-2],[0,2]], 
            [[0,0],[-1,0],[1,0],[0,1],[0,-1],[-1,-1],[-1,1],[1,-1],[1,1],[-2,0],[2,0],[0,-2],[0,2],[-2,-2],[-2,-1],[-1,-2],[2,-2],[2,-1],[1,-2],[-2,2],[-2,1],[-1,2],[2,2],[2,1],[1,2]] 
            ]
        self.mode_name = {QtWidgets.QGraphicsView.NoDrag: "No Drag Mode",
        QtWidgets.QGraphicsView.ScrollHandDrag: "ScrollHand Drag Mode",
        QtWidgets.QGraphicsView.RubberBandDrag: "RubberBand Drag Mode"}

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
                self.save_factor[0] = factor*self._zoom
                self.save_factor[1] = factor*self._zoom
            else:
                factor = 0.8
                self._zoom -= 1
                self.save_factor[0] = factor*self._zoom
                self.save_factor[1] = factor*self._zoom
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom <= 0:
                self.fitInView()
                self.save_factor = [1,1]
    
    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.mouse_button = event.button()
            if self.dragMode() == QtWidgets.QGraphicsView.NoDrag:
                self.photoClicked.emit(self.mapToScene(event.pos()).toPoint()) # 포토가 클릭되었고 그 위치를 시그널로 전달 
            elif self.dragMode() == QtWidgets.QGraphicsView.RubberBandDrag: 
                if self.len_start_pos == None:
                    self.len_start_pos = self.mapToScene(event.pos()).toPoint()

        super(PhotoViewer, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.dragMode() == QtWidgets.QGraphicsView.RubberBandDrag:
            self.rubberBandCheck.emit(self.mapToScene(event.pos()).toPoint()) # 포토가 클릭되었고 그 위치를 시그널로 전달 
        super(PhotoViewer, self).mouseReleaseEvent(event)


class Widget_mask(QtWidgets.QWidget):
    sliderChangedMask = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setRange(0, 255)
        self.slider.setSingleStep(1)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksRight)
        self.slider.valueChanged.connect(self.updateLabel)
        self.label = QtWidgets.QLabel('0', self)

        self.btnChange = QtWidgets.QToolButton(self)
        self.btnChange.setText('apply threshold')
        self.btnChange.clicked.connect(self.sendSliderValue)

        layout_v= QtWidgets.QVBoxLayout(self)
        layout_h = QtWidgets.QHBoxLayout()

        layout_h.addWidget(self.slider)
        layout_h.addSpacing(15)
        layout_h.addWidget(self.label)

        layout_v.addLayout(layout_h)
        layout_v.addWidget(self.btnChange)

    
    def sendSliderValue(self):
        self.sliderChangedMask.emit(int(self.slider.value()))

    def updateLabel(self, value):
        self.label.setText(str(value))



class Widget_merge(QtWidgets.QWidget):
    sliderChangedMerge = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setRange(0, 100)
        self.slider.setSingleStep(1)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksRight)
        self.slider.valueChanged.connect(self.updateLabel)
        self.label = QtWidgets.QLabel('0', self)

        self.btnChange = QtWidgets.QToolButton(self)
        self.btnChange.setText('apply transparency')
        self.btnChange.clicked.connect(self.sendSliderValue)

        self.btnDefault = QtWidgets.QToolButton(self)
        self.btnDefault.setText('default')
        self.btnDefault.clicked.connect(self.default)

        layout_v= QtWidgets.QVBoxLayout(self)
        layout_h = QtWidgets.QHBoxLayout()

        layout_h.addWidget(self.slider)
        layout_h.addSpacing(15)
        layout_h.addWidget(self.label)

        layout_h2 = QtWidgets.QHBoxLayout()
        layout_h2.addWidget(self.btnChange)
        layout_h2.addWidget(self.btnDefault)

        layout_v.addLayout(layout_h)
        layout_v.addLayout(layout_h2)
    def default(self):
        self.slider.setValue(50)
        self.sliderChangedMerge.emit(50)
        self.label.setText(str(float(self.slider.value())/100))

    def sendSliderValue(self):
        self.sliderChangedMerge.emit(self.slider.value())

    def updateLabel(self, value):
        self.label.setText(str(float(self.slider.value())/100))


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.on_screen = None
        self.on_mode = None

        self.viewer = PhotoViewer(self)
        # 'Load image' button
        self.btnLoad = QtWidgets.QToolButton(self)
        self.btnLoad.setText('Original image')
        self.btnLoad.clicked.connect(self.loadImage)

        # 'generate mask' button
        self.btnGen = QtWidgets.QToolButton(self)
        self.btnGen.setText('Generated mask')
        self.btnGen.clicked.connect(self.generateMask)

        # 'merge image mask' button
        self.btnMerge = QtWidgets.QToolButton(self)
        self.btnMerge.setText('Overlay image')
        self.btnMerge.clicked.connect(self.mergeImageMask)

        # Button to change from drag/pan to getting pixel info
        self.btnPixInfo = QtWidgets.QToolButton(self)
        self.btnPixInfo.setText('pixel annotate mode')
        self.btnPixInfo.clicked.connect(self.pixInfo)
        self.editPixInfo = QtWidgets.QLineEdit(self)
        self.editPixInfo.setReadOnly(True)
        self.viewer.photoClicked.connect(self.photoClicked)
        self.viewer.rubberBandCheck.connect(self.rubberBandCheck)

        # 'analysis' button
        self.btnAnalysis = QtWidgets.QToolButton(self)
        self.btnAnalysis.setText('Analysis')
        self.btnAnalysis.clicked.connect(self.particle_analysis)

        # 'pixel-length' button
        self.btnPixlen = QtWidgets.QToolButton(self)
        self.btnPixlen.setText('pixel-length')
        self.btnPixlen.clicked.connect(self.plxel_length)


        # 'remove-length' button
        self.btnRemovelen = QtWidgets.QToolButton(self)
        self.btnRemovelen.setText('remove-length')
        self.btnRemovelen.clicked.connect(self.remove_length)

        # 'drag-annotate' button
        self.btnDragAnnotate = QtWidgets.QToolButton(self)
        self.btnDragAnnotate.setText('drag-annotate')
        self.btnDragAnnotate.clicked.connect(self.drag_annotate)


        # 'scroll-mode' button
        self.btnScrollMode = QtWidgets.QToolButton(self)
        self.btnScrollMode.setText('scroll-mode')
        self.btnScrollMode.clicked.connect(self.scroll_mode)


        # Status bar
        self.status_bar = QtWidgets.QStatusBar(self)
        #self.setStatusBar(status_bar)

        # Menu bar
        menu_open_action = QAction('&Open', self)
        menu_open_action.setShortcut('Ctrl+O')
        menu_open_action.setStatusTip('open an image')
        menu_open_action.triggered.connect(self.menu_open_image)

        menu_save_action = QAction('&Save', self)
        menu_save_action.setShortcut('Ctrl+S')
        menu_save_action.setStatusTip('save an image')
        menu_save_action.triggered.connect(self.menu_save_image)

        menu_mask_open_action = QAction('&Open mask', self)
        menu_mask_open_action.setStatusTip('mask from outer image')
        menu_mask_open_action.triggered.connect(self.menu_mask_open)

        menu_MP_VAT_action = QAction('&MP_VAT', self)
        menu_MP_VAT_action.setStatusTip('MP_VAT from original')
        menu_MP_VAT_action.triggered.connect(self.menu_MP_VAT)

        menu_MP_VAT_2_action = QAction('&MP_VAT_2', self)
        menu_MP_VAT_2_action.setStatusTip('MP_VAT_2 from original')
        menu_MP_VAT_2_action.triggered.connect(self.menu_MP_VAT_2)

        menu_UNet_action = QAction('&UNet', self)
        menu_UNet_action.setStatusTip('UNet from original')
        menu_UNet_action.triggered.connect(self.menu_UNet)

        menu_custom_treshold_action = QAction('&custom_treshold', self)
        menu_custom_treshold_action.setStatusTip('custom_treshold from original')
        menu_custom_treshold_action.triggered.connect(self.menu_custom_treshold)

        menu_custom_transparency_action = QAction('&custom_transparency', self)
        menu_custom_transparency_action.setStatusTip('custom_transparency from original')
        menu_custom_transparency_action.triggered.connect(self.menu_custom_transparency)

        menu_brush_size_up_action = QAction('&brush size up', self)
        menu_brush_size_up_action.setShortcut('Ctrl+E')
        menu_brush_size_up_action.setStatusTip('encrease the brush size')
        menu_brush_size_up_action.triggered.connect(self.menu_brush_size_up)

        menu_brush_size_down_action = QAction('&brush size down', self)
        menu_brush_size_down_action.setShortcut('Ctrl+D')
        menu_brush_size_down_action.setStatusTip('decrease the brush size')
        menu_brush_size_down_action.triggered.connect(self.menu_brush_size_down)

        menu_create_training_patches_action = QAction('&Create training patches', self)
        menu_create_training_patches_action.setStatusTip('Create image-mask pair patches for training')
        menu_create_training_patches_action.triggered.connect(self.menu_create_training_patches)

        menu_set_mouse_scroll_action = QAction('&set mouse scroll', self)
        menu_set_mouse_scroll_action.setShortcut('Alt+S')
        menu_set_mouse_scroll_action.setStatusTip('set mouse scroll')
        menu_set_mouse_scroll_action.triggered.connect(self.menu_set_mouse_scroll)

        menu_set_mouse_measure_length_action = QAction('&set mouse measure length', self)
        menu_set_mouse_measure_length_action.setShortcut('Alt+M')
        menu_set_mouse_measure_length_action.setStatusTip('set mouse measure length')
        menu_set_mouse_measure_length_action.triggered.connect(self.menu_set_mouse_measure_length)

        menu_set_mouse_remove_original_action = QAction('&set mouse remove original', self)
        menu_set_mouse_remove_original_action.setShortcut('Alt+R')
        menu_set_mouse_remove_original_action.setStatusTip('set mouse remove original')
        menu_set_mouse_remove_original_action.triggered.connect(self.menu_set_mouse_remove_original)

        menu_set_mouse_pix_annotate_action = QAction('&set mouse pix annotate', self)
        menu_set_mouse_pix_annotate_action.setShortcut('Ctrl+Alt+A')
        menu_set_mouse_pix_annotate_action.setStatusTip('set mouse pix annotate')
        menu_set_mouse_pix_annotate_action.triggered.connect(self.menu_set_mouse_pix_annotate)

        menu_set_mouse_drag_annotate_action = QAction('&set mouse drag annotate', self)
        menu_set_mouse_drag_annotate_action.setShortcut('Ctrl+Alt+D')
        menu_set_mouse_drag_annotate_action.setStatusTip('set mouse drag annotate')
        menu_set_mouse_drag_annotate_action.triggered.connect(self.menu_set_mouse_drag_annotate)        

        menu_bar = QtWidgets.QMenuBar(self)
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(menu_open_action)
        file_menu.addAction(menu_save_action)

        file_menu = menu_bar.addMenu('&Mask')
        file_menu.addAction(menu_mask_open_action)
        file_menu.addAction(menu_MP_VAT_action)
        file_menu.addAction(menu_MP_VAT_2_action)        
        file_menu.addAction(menu_UNet_action)
        file_menu.addAction(menu_custom_treshold_action)          

        file_menu = menu_bar.addMenu('&Annotate')
        file_menu.addAction(menu_custom_transparency_action)
        file_menu.addAction(menu_brush_size_up_action)
        file_menu.addAction(menu_brush_size_down_action)

        file_menu = menu_bar.addMenu('&ModelTraining')
        file_menu.addAction(menu_create_training_patches_action)

        file_menu = menu_bar.addMenu('&MouseMode')
        file_menu.addAction(menu_set_mouse_scroll_action)
        file_menu.addAction(menu_set_mouse_measure_length_action)
        file_menu.addAction(menu_set_mouse_remove_original_action)
        file_menu.addAction(menu_set_mouse_pix_annotate_action)
        file_menu.addAction(menu_set_mouse_drag_annotate_action)



        self.widget_mask = Widget_mask()
        self.widget_mask.sliderChangedMask.connect(self.sliderChangedMask)
        
        self.widget_merge = Widget_merge()
        self.widget_merge.sliderChangedMerge.connect(self.sliderChangedMerge)


        # Arrange layout
        VBlayout = QtWidgets.QVBoxLayout(self)     
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout_2 = QtWidgets.QHBoxLayout()
        HBlayout.setAlignment(QtCore.Qt.AlignLeft)
        HBlayout_2.setAlignment(QtCore.Qt.AlignLeft)

        HBlayout.addWidget(self.btnLoad)
        HBlayout.addWidget(self.btnGen)
        HBlayout.addWidget(self.btnMerge)
        HBlayout.addWidget(self.btnAnalysis)

        HBlayout_2.addWidget(self.btnScrollMode)
        HBlayout_2.addWidget(self.btnPixlen)
        HBlayout_2.addWidget(self.btnRemovelen)
        HBlayout_2.addWidget(self.btnPixInfo)
        HBlayout_2.addWidget(self.btnDragAnnotate)
        
        HBlayout.addWidget(self.editPixInfo)
        VBlayout.addWidget(menu_bar)
        VBlayout.addLayout(HBlayout)
        VBlayout.addLayout(HBlayout_2)
        VBlayout.addWidget(self.viewer)
        VBlayout.addWidget(self.status_bar)

        self.status_bar.showMessage("ready")

    def menu_open_image(self):
        self.status_bar.showMessage("menu open")
        self.viewer.ori_image = None
        self.loadImage()

    def menu_save_image(self):
        self.status_bar.showMessage("menu save")        
        self.saveImage()

    def menu_mask_open(self):
        #error -> size맞지 않는지, ori image가 있는지?
        self.status_bar.showMessage("menu mask open")                
        fname = QFileDialog.getOpenFileName(self, 'Open mask file', './')
        if (fname[0]) == '':
            return
        pixmap = QtGui.QPixmap(fname[0])
        self.viewer.mask_image = self.pixmap2ndarray(pixmap)
        self.viewer.merged_image = None
        self.viewer.setPhoto(pixmap)   

    def menu_MP_VAT(self):
        self.status_bar.showMessage("menu MP-VAT")
        self.viewer.mask_image =None
        self.generateMask(MP_VAT)

    def menu_MP_VAT_2(self):
        self.status_bar.showMessage("menu MP-VAT 2")
        self.viewer.mask_image =None
        self.generateMask(MP_VAT_2)

    def menu_UNet(self):
        self.status_bar.showMessage("menu UNet")
        self.viewer.mask_image =None
        self.generateMask(UNet)

    def menu_custom_treshold(self):
        self.status_bar.showMessage("menu custom treshold")
        self.viewer.mask_image =None
        self.widget_mask.show()

    def menu_custom_transparency(self):
        self.status_bar.showMessage("menu custom transparency")   
        self.viewer.merged_image =None
        self.widget_merge.show()     

    def menu_brush_size_up(self):
        if (self.viewer.brush_size < 4):
            self.viewer.brush_size +=1
        
    def menu_brush_size_down(self):
        if (self.viewer.brush_size > 0):
            self.viewer.brush_size -=1

    def menu_create_training_patches(self):
        self.status_bar.showMessage("NotImplemented: menu_create_training_patches")
        ori_image  = self.viewer.ori_image
        mask_image  = self.viewer.mask_image
        parameter_tuning(ori_image, mask_image)


    # 5 Mouse modes on the menubar
    def menu_set_mouse_scroll(self):
        self.status_bar.showMessage("mouse scroll")
        self.scroll_mode()

    def menu_set_mouse_measure_length(self):
        self.status_bar.showMessage("mouse measure length")
        self.plxel_length()

    def menu_set_mouse_remove_original(self):
        self.status_bar.showMessage("mouse remove original")
        self.remove_length()

    def menu_set_mouse_pix_annotate(self):
        self.status_bar.showMessage("mouse pix annotate")
        self.pixInfo()

    def menu_set_mouse_drag_annotate(self):
        self.status_bar.showMessage("mouse drag annotate")
        self.drag_annotate()



    def sliderChangedMask(self,value):
        self.viewer.mask_image =None
        self.generateMask(value)

    def sliderChangedMerge(self,value):
        self.viewer.merged_image =None
        self.viewer.merge_alpha = float(value) / 100
        self.mergeImageMask()

    def show_ndarray_on_screen(self,arr):
        qimage_var = qimage2ndarray.array2qimage(arr, normalize=False)
        qpixmap_var = QtGui.QPixmap.fromImage(qimage_var)            
        self.viewer._photo.setPixmap(qpixmap_var)        

    def pixmap2ndarray(self,pixmap):
        rec_arr = qimage2ndarray.recarray_view(pixmap.toImage())
        r,g,b = rec_arr["r"], rec_arr["g"], rec_arr["b"]
        rgb_uint8 = np.dstack((r,g,b)).astype(np.uint8)
        return rgb_uint8


    # 5 Mouse modes
    def scroll_mode(self):
        self.on_mode = "scroll-mode"
        self.viewer.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def drag_annotate(self):
        self.on_mode = "drag-annotate"
        self.viewer.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

    def pixInfo(self):
        #self.viewer.toggleDragMode()
        self.on_mode = "pixel annotate"
        self.viewer.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.status_bar.showMessage("pixel annotate mode")

    def plxel_length(self):
        #self.viewer.toggleRubberMode()
        self.viewer.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.on_mode = "pixlen"
        self.status_bar.showMessage("measure pixel length")

    def remove_length(self):
        #self.viewer.toggleRubberMode()
        self.viewer.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.on_mode = "removelen"
        self.status_bar.showMessage("Remove area")
        self.viewer.mask_image = None


    def loadImage(self):
        if self.viewer.ori_image is None:
            fname = QFileDialog.getOpenFileName(self, 'Open file', './')
            if fname[0] == '':
                return            
            pixmap = QtGui.QPixmap(fname[0])
            #pixmap = QtGui.QPixmap('023_fl.png')# 대화상자 지워버렸네..

            self.viewer.ori_image = self.pixmap2ndarray(pixmap)
            self.viewer.setPhoto(pixmap)   
        else:
            self.show_ndarray_on_screen(self.viewer.ori_image)

        self.on_screen = "ori"

    def saveImage(self):
        FileSave = QFileDialog.getSaveFileName(self, 'Save file', './',"png files (*.png)")
        if FileSave[0] == '':
            return
        saveImgDic = {"ori":self.viewer.ori_image,
        "mask":self.viewer.mask_image,
        "merged":self.viewer.merged_image,
        "analysis":self.viewer.labeled_image
        }

        target_pixels = saveImgDic[self.on_screen]
        if self.on_screen != 'analysis':
            im = Image.fromarray(target_pixels.astype(np.uint8))
            im.save(FileSave[0])
        else:
            add_grid(target_pixels,FileSave[0])

    def generateMask(self, mask_function = None):
        if self.viewer.mask_image is None:
            if str(type(mask_function)) == "<class 'int'>":
                value = mask_function
                self.viewer.mask_image = custom_thresholding(self.viewer.ori_image, value)
            else:
                if str(type(mask_function)) != "<class 'function'>":
                    mask_function = MP_VAT
                self.viewer.mask_image = mask_function(self.viewer.ori_image)
        self.show_ndarray_on_screen(self.viewer.mask_image)
        self.on_screen = "mask"

    def mergeImageMask(self):
        if self.viewer.merged_image is None or self.on_screen == "mask":
            ori_arr = self.viewer.ori_image
            mask_arr = self.viewer.mask_image
            ret_arr = ori_arr*self.viewer.merge_alpha + mask_arr*(1-self.viewer.merge_alpha)

            self.viewer.merged_image = ret_arr

        self.show_ndarray_on_screen(self.viewer.merged_image)
        self.on_screen = "merged"


    def particle_analysis(self):
        #temp_zoom = self.viewer._zoom
        if self.viewer.mask_image is None or self.viewer.ori_image is None :
            self.raise_error("no mask error")
            return
       
        self.viewer.labeled_image = MP_ACT(self.viewer.mask_image, self.viewer.ori_image,self.viewer.micrometer_per_pix)
        self.show_ndarray_on_screen(self.viewer.labeled_image)
        self.on_screen = "analysis"

    def raise_error(self,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()



    def photoClicked(self, pos):
        #self.status_bar.showMessage(self.viewer.mode_name[self.viewer.dragMode()])
        if self.viewer.dragMode()  == QtWidgets.QGraphicsView.NoDrag:
            self.status_bar.showMessage(self.on_mode)
            self.editPixInfo.setText('%d, %d' % (pos.x(), pos.y()))
            if self.on_mode == "pixel annotate": #merge모드일경우에만 수정가능 
                # 해당 위치에 상응하는 original image, mask, merged의 픽셀을 255 또는 0으로 변경 

                alpha = self.viewer.merge_alpha
                ori_arr =self.viewer.ori_image
                mask_arr =self.viewer.mask_image
                ret_arr =self.viewer.merged_image
                button = self.viewer.mouse_button
                x,y  = pos.x(), pos.y()
                shape_y, shape_x = self.viewer.merged_image.shape[0],self.viewer.merged_image.shape[1]

                for dx,dy  in self.viewer.brush_levels[self.viewer.brush_size]:
                    if (y+dy>=0 and y+dy < shape_y and x+dx>=0 and x+dx < shape_x):
                        if button == 1:
                            mask_arr[y+dy][x+dx] = np.asarray([0,0,0])
                        elif button == 2:
                            mask_arr[y+dy][x+dx] = np.asarray([255,255,255])

                        ret_arr[y+dy][x+dx] = ori_arr[y+dy][x+dx]*alpha + mask_arr[y+dy][x+dx]*(1-alpha)

                self.viewer.mask_image = mask_arr                
                self.viewer.merged_image = ret_arr                
                
                self.show_ndarray_on_screen(self.viewer.merged_image)
            
    def rubberBandCheck(self, pos):
        if self.viewer.dragMode()  == QtWidgets.QGraphicsView.RubberBandDrag:
            if (self.viewer.len_start_pos is None):
                return
            start_x, start_y = self.viewer.len_start_pos.x(),self.viewer.len_start_pos.y()
            end_x,end_y = pos.x(), pos.y()

            if end_y < start_y:
                end_y , start_y = start_y , end_y

            if end_x < start_x:
                end_x , start_x = start_x , end_x

            if self.on_mode == "drag-annotate":
                alpha = self.viewer.merge_alpha
                ori_arr =self.viewer.ori_image
                mask_arr =self.viewer.mask_image
                ret_arr =self.viewer.merged_image
                button = self.viewer.mouse_button

                if button == 1:
                    mask_arr[start_y:end_y, start_x:end_x] = np.asarray([0,0,0])
                elif button == 2:
                    mask_arr[start_y:end_y, start_x:end_x] = np.asarray([255,255,255])

                ret_arr[start_y:end_y, start_x:end_x] = ori_arr[start_y:end_y, start_x:end_x]*alpha + mask_arr[start_y:end_y, start_x:end_x]*(1-alpha)

                self.viewer.mask_image = mask_arr                
                self.viewer.merged_image = ret_arr                
                self.show_ndarray_on_screen(self.viewer.merged_image)
                pass

            elif self.on_mode == "pixlen":
                pixlen = np.sqrt(np.power(start_y - end_y,2) + np.power(start_x - end_x,2))
                self.viewer.len_start_pos = None
                micrometer, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter the micrometer')

                #크리랑 이야기해봐야할 듯 이부분은 
                if ok:
                    self.viewer.micrometer_per_pix = float(micrometer) / pixlen

            elif self.on_mode == "removelen":
                self.viewer.ori_image[start_y:end_y, start_x:end_x] = np.asarray([0,0,0])
                self.show_ndarray_on_screen(self.viewer.ori_image)

            self.viewer.len_start_pos = None


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setWindowTitle("You Only Label Once - Trainable overlay annotator")
    window.setGeometry(500, 300, 1200, 800)
    window.show()
    sys.exit(app.exec_())