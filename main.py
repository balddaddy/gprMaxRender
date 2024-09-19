# import necessary modules
import sys
import math
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mainWindow import Ui_MainWindow # import UI model
import renderAlgorithm as alg        # import algorithm
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import importlib.util

# define main window class
class MainWindow(QMainWindow, Ui_MainWindow):
    # mainWindow constructor
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("gprMaxRender")
        self.statusbar.showMessage("Ready")
        self.actionLoad.triggered.connect(self.loadFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionExit.triggered.connect(self.closeApp)
        self.pushButton_Render.clicked.connect(self.renderOnce)
        self.initVTKWidget()

    # initialize VTK widget, which is a QVTKRenderWindowInteractor
    def initVTKWidget(self, ):
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        layout = QVBoxLayout(self.frame)
        layout.addWidget(self.vtkWidget)
        self.vtkWidget.show()

    # paint a cube in VTK to show the domain
    def domain(self, cmd):
        cmds = cmd.split()
        # set VTK source
        source = vtk.vtkCubeSource()
        xMin, xMax = 0., float(cmds[1])  # 使用float()函数转换字符串为浮点数
        yMin, yMax = 0., float(cmds[2])
        zMin, zMax = 0., float(cmds[3])
        source.SetXLength(xMax-xMin)
        source.SetYLength(yMax-yMin)
        source.SetZLength(zMax-zMin)
        source.SetCenter(xMin+xMax/2, yMin+yMax/2, zMin+zMax/2)

        # mapping data to vtk
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        # create actor and set mapper
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetOpacity(0.2)
        # add actor to renderer
        self.ren.AddActor(actor)  
        self.ren.SetBackground(0.1, 0.1, 0.2)
        self.ren.SetBackground2(0.4, 0.4, 0.6)
        self.ren.SetGradientBackground(True)
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()
    
    # paint a cylinder in VTK
    def cyliner(self, cmd):
        cmds = cmd.split()
        xMin, xMax = float(cmds[1]), float(cmds[4])
        yMin, yMax = float(cmds[2]), float(cmds[5])
        zMin, zMax = float(cmds[3]), float(cmds[6])
        radius = float(cmds[7])
        height = math.sqrt((xMax - xMin)**2 + (yMax - yMin)**2 + (zMax - zMin)**2)
        # set VTK source
        source = vtk.vtkCylinderSource()
        source.SetRadius(radius)
        source.SetHeight(height)
        source.SetResolution(100)

        # create a transform and move the cylinder to the poper position
        half_height = height / 2
        [angleX, angleY, angleZ] = alg.CalculateAngle(xMin, xMax, yMin, yMax, zMin, zMax)
        transform = vtk.vtkTransform()
        transform.Translate(0, 0, half_height)
        transform.RotateX(angleZ)
        transform.RotateZ(angleX)
        [moveX, moveY, moveZ] = alg.CalculateMovement(xMin, yMin, zMin, angleZ, 0.0, angleX)
        transform.Translate(moveX, moveY, -moveZ)

        # apply transform to the source
        transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetInputConnection(source.GetOutputPort())
        transformFilter.SetTransform(transform)

        # mapping data to vtk
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(transformFilter.GetOutputPort())

        # create actor and set mapper
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1.0, 0.0, 0.0)
        actor.GetProperty().SetOpacity(0.8)

        # add actor to renderer
        self.ren.AddActor(actor)
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()

    # paint a sphere in VTK
    def sphere(self, cmd):
        cmds = cmd.split()
        centerX = float(cmds[1])
        centerY = float(cmds[2])
        centerZ = float(cmds[3])
        radius = float(cmds[4])
        # set VTK source
        source = vtk.vtkSphereSource()
        source.SetRadius(radius)
        source.SetCenter(centerX, centerY, -centerZ)

        # mapping data to vtk
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        # create actor and set mapper
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.0, 1.0, 0.0)
        actor.GetProperty().SetOpacity(0.8)

        # add actor to renderer
        self.ren.AddActor(actor)
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()

    def box(self, cmd):
        cmds = cmd.split()
        # set VTK source
        source = vtk.vtkCubeSource()
        xMin, xMax = float(cmds[1]), float(cmds[4])  # 使用float()函数转换字符串为浮点数
        yMin, yMax = float(cmds[2]), float(cmds[5])
        zMin, zMax = float(cmds[3]), float(cmds[6])
        source.SetXLength(xMax-xMin)
        source.SetYLength(yMax-yMin)
        source.SetZLength(zMax-zMin)
        source.SetCenter(xMin+xMax/2, yMin+yMax/2, zMin+zMax/2)

        # mapping data to vtk
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        # create actor and set mapper
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.8, 0.9, 0.7)
        actor.GetProperty().SetOpacity(0.8)

        # add actor to renderer
        self.ren.AddActor(actor)  
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()

    def updataStatusBar(self, msg):
        self.statusbar.showMessage(msg, 2000);

    def closeApp(self):
        self.updataStatusBar("Byebye")
        sys.exit()

    def loadFile(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "*.in")
        if fname[0]:
            with open(fname[0], "r") as file:
                text = file.read()
                self.plainTextEdit.setPlainText(text)
                self.updataStatusBar(f"Loaded {fname}")

    def saveFile(self):
        fname = QFileDialog.getSaveFileName(self, "Save File", "", "*.in")
        if fname[0]:
            with open(fname[0], "w") as file:
                text = self.plainTextEdit.toPlainText()
                file.write(text)
                self.updataStatusBar(f"Saved {fname}")

    def renderOnce(self):
        inputTxt = self.plainTextEdit.toPlainText()
        self.updataStatusBar("Rendering Input Models...")
        alg.renderOnce(self, inputTxt)
        


                
def main():
    module_path = importlib.util.find_spec('vtk.qt')
    if module_path:
        print(f"The path of'my_custom_module' is: {module_path.submodule_search_locations[0]}")
    else:
        print("The'my_custom_module' was not found.")
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()