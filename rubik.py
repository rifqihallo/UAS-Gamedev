from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import LerpHprInterval, Func, Sequence
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.task import Task
from math import pi, sin, cos
from direct.gui.OnscreenText import OnscreenText,TextNode
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage

import sys


def crearCube(parent, x, y, z, position, cubeCondition, walls):
	#mengembalikan format simpul standar dengan warna yang ada, normal 3-komponen, dan posisi simpul 3-komponen.
	vformat = GeomVertexFormat.getV3n3cp()
	# digunakan untuk menyimpan informasi warna dalam tabel data
	vdata = GeomVertexData("cube_data", vformat, Geom.UHStatic)
	#
	tris = GeomTriangles(Geom.UHStatic)
	# GeomTriangles menyimpan sejumlah data yang terhubung
	# GeomVertexWriter menghasilkan pointer ke objek vdata untuk menulis data
	posWriter = GeomVertexWriter(vdata, "vertex")
	colWriter = GeomVertexWriter(vdata, "color")
	normalWriter = GeomVertexWriter(vdata, "normal")

	vcount = 0
	contador = 0

	for direccion in (1, -1):
		for i in range(3):
			normal = VBase3()
			normal[i] = direccion
			rgb = [0., 0., 0.]

			#Memberi warna pada kubus
			if direccion == -1:
				if i == 0:
					color = (1, .5, .0, 1.) #Oranye
				elif i == 1:
					color =  (.024, .235, 1, 1.) #Biru
				elif i == 2:
					contador = contador + 1
					if contador == 1:
						color =  (255, 255, 0, 1.) #Kuning

			elif i == 1:
				color = (0, 1, 0, 1) #Hijau
			elif i == 0:
				color = (255, 0, 0	, 1.) #Merah
			elif i == 2:
				color = (255, 255, 255, 1.) #Putih
			else:
				pass


			for a, b in ((-1., -1.), (-1., 1.), (1., 1.), (1., -1.)):
				pos = VBase3()
				pos[i] = direccion
				pos[(i + direccion) % 3] = a
				pos[(i + direccion * 2) % 3] = b

				posWriter.addData3f(pos)
				colWriter.addData4f(color)
				normalWriter.addData3f(normal)

			vcount += 4

			tris.addVertices(vcount - 2, vcount - 3, vcount - 4)
			tris.addVertices(vcount - 4, vcount - 1, vcount - 2)

	geom = Geom(vdata)
	# mengumpulkan geomVertexdata dan satu atau lebih objek GeomPrimitive untuk membuat port geometrik tunggal.
	geom.addPrimitive(tris)
	# Menyimpan objek geometri yang dapat dirender
	node = GeomNode("cube_node")
	node.addGeom(geom)
	cube = parent.attachNewNode(node)
	cube.setScale(.48)
	cube.setPos(x, y, z)
	Condition = set()  # Menentukan kondisi kubus
	position[cube] = [x, y, z]
	cubeCondition[cube] = Condition

	# sumbu X menunjuk langsung ke kanan.
        # Sumbu Y tegak lurus dengan layar.
        # Sumbu Z mengarah ke atas.

	if x == 1:
		walls["right"].append(cube)
		Condition.add("right")
	elif x == -1:
		walls["left"].append(cube)
		Condition.add("left")
	elif x == 0:
		walls["center"].append(cube)
		Condition.add("center")

	if y == 1:
		walls["back"].append(cube)
		Condition.add("back")
	elif y == -1:
		walls["front"].append(cube)
		Condition.add("front")
	elif y == 0:
		walls["standing"].append(cube)
		Condition.add("standing")

	if z == -1:
		walls["down"].append(cube)
		Condition.add("down")
	elif z == 1:
		walls["up"].append(cube)
		Condition.add("up")
	elif z == 0:
		walls["equator"].append(cube)
		Condition.add("equator")

	return cube


class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		# Menentukan key exit
		self.accept("escape", sys.exit)

		#Memuat waktu layar
		for i in range(0,15):
			self.loadscreen()

		

		# Untuk Instruksi program
		info = OnscreenText(text="Tombol:",
		                    style=1, fg=(1, 1, 1, 1), pos=(-1.1, .90), scale=.07)
		up = OnscreenText(text="-Atas: U",
		                  style=1, fg=(1, 1, 1, 1), pos=(-1.1, .80), scale=.05)
		down = OnscreenText(text="-Bawah: D,",
		                    style=1, fg=(1, 1, 1, 1), pos=(-1.1, .70), scale=.05)
		left = OnscreenText(text="    -Kiri: L",
		                    style=1, fg=(1, 1, 1, 1), pos=(-1.1, .60), scale=.05)
		right = OnscreenText(text="    -Kanan: R",
		                     style=1, fg=(1, 1, 1, 1), pos=(-1.1, .50), scale=.05)
		front = OnscreenText(text="-Depan: F",
		                     style=1, fg=(1, 1, 1, 1), pos=(-1.1, .40), scale=.05)
		back = OnscreenText(text="-Latar Belakang: B",
		                    style=1, fg=(1, 1, 1, 1), pos=(-1.1, .30), scale=.05)
		equator = OnscreenText(text="    - Pusat-E: E",
		                       style=1, fg=(1, 1, 1, 1), pos=(-1.1, .20), scale=.05)
		standing = OnscreenText(text="   - Pusat-S: S",
		                        style=1, fg=(1, 1, 1, 1), pos=(-1.1, .10), scale=.05)
		center = OnscreenText(text="   - Pusat-C: C",
		                      style=1, fg=(1, 1, 1, 1), pos=(-1.1, .0), scale=.05)
		vista = OnscreenText(text="- Mulai Ulang Tampilan: K",
		                      style=1, fg=(1, 1, 1, 1), pos=(-1.1, -.10), scale=.05)
		voltear = OnscreenText(text="- Kembali: Z",
		                      style=1, fg=(1, 1, 1, 1), pos=(-1.1, -.20), scale=.05)
		inst1 = OnscreenText(text="                  Press Key then Enter",
		                     style=1, fg=(1, 1, 1, 1), pos=(-1.1, -.70), scale=.05)
		info3 = OnscreenText(text="ESC untuk keluar ",
		                     style=1, fg=(1, 1, 1, 1), pos=(1, -.90), scale=.05)
		# Load background image
		try:
			b = OnscreenImage(parent=render2d, image="bg.jpg")
		except:
			pass
		walls = {}
		pivotes = {}
		rotaciones = {}
		position = {}
		cubeCondition = {}
		wallIDs = ("front", "back", "left", "right", "down", "up", "equator", "center", "standing")
		movement = {}
                # Jika berputar di sekitar sumbu 90 derajat, VBase3 (90., 0., 0.).
                # Nilainya positif mengikuti aturan tangan kanan.
		movement["right"] = VBase3(0., -90., 0.)
		movement["center"] = VBase3(0., -90., 0.)  # Arah putaran bagian "tengah" mengikuti bagian "kanan".
		movement["left"] = VBase3(0., 90., 0.)
		movement["back"] = VBase3(0., 0., -90.)
		movement["front"] = VBase3(0., 0., 90.)
		movement["standing"] = VBase3(0., 0., 90.)  # Arah putaran bagian bawah mengikuti muka "depan".
		movement["down"] = VBase3(90., 0., 0.)
		movement["up"] = VBase3(-90., 0., 0.)
		movement["equator"] = VBase3(-90., 0., 0.)  # Arah putaran pusat "tengah" mengikuti wajah "atas".
		wallRotacion = {}
		wallNegRotacion = {}
                # Setiap rotasi adalah matriks.
                # Rotasi positif "depan" dan rotasi negatif "belakang" memiliki matriks yang sama.
                # Irisan "stading" mengikuti aturan bagian "depan".

		wallRotacion["right"] = wallRotacion["center"] = wallNegRotacion["left"] = [[1, 0, 0], [0, 0, -1], [0, 1, 0]]
		wallRotacion["left"] = wallNegRotacion["right"] = wallNegRotacion["center"] = [[1, 0, 0], [0, 0, 1], [0, -1, 0]]

		wallRotacion["back"] = wallNegRotacion["standing"] = wallNegRotacion["front"] = [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]
		wallRotacion["front"] = wallRotacion["standing"] = wallNegRotacion["back"] = [[0, 0, -1], [0, 1, 0], [1, 0, 0]]

		wallRotacion["up"] = wallRotacion["equator"] = wallNegRotacion["down"] = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
		wallRotacion["down"] = wallNegRotacion["equator"] = wallNegRotacion["up"] = [[0, 1, 0], [-1, 0, 0], [0, 0, 1]]

		for wallID in wallIDs:
			walls[wallID] = []
			pivotes[wallID] = self.render.attachNewNode('pivot_%s' % wallID)
			rotaciones[wallID] = {"hpr": movement[wallID]}
		# print walls
		# print pivots
		# print rotations
		for x in (-1, 0, 1):
			for y in (-1, 0, 1):
				for z in (-1, 0, 1):
					crearCube(self.render, x, y, z, position, cubeCondition, walls)
                # Pengaturan arah kamera
		self.cam.setPos(7, -10, 6)
		self.cam.lookAt(0., 0., 0.)


		def reparentcubes(wallID):
			pivote = pivotes[wallID]
			children = pivote.getChildren()
			children.wrtReparentTo(self.render)
			pivote.clearTransform()
			children.wrtReparentTo(pivote)
			for cube in walls[wallID]:
				cube.wrtReparentTo(pivote)

		def UpdatedConditioncube(wallID, negRotacion=False):
			for cube in walls[wallID]:
				ConditionAnterior = cubeCondition[cube]
				ConditionUpdated = set()
				cubeCondition[cube] = ConditionUpdated

				# koordinat dari X
				newPos = 0
				if not negRotacion:
					for j in range(3):
						newPos = newPos + int(position[cube][j]) * int(wallRotacion[wallID][j][0])
				else:
					for j in range(3):
						newPos = newPos + int(position[cube][j]) * int(wallNegRotacion[wallID][j][0])

				if newPos == 1:
					ConditionUpdated.add("right")
				elif newPos == -1:
					ConditionUpdated.add("left")
				elif newPos == 0:
					ConditionUpdated.add("center")
				newPosX = newPos

				# koordinat dari Y
				newPos = 0
				if not negRotacion:
					for j in range(3):
						newPos = newPos + int(position[cube][j]) * int(wallRotacion[wallID][j][1])
				else:
					for j in range(3):
						newPos = newPos + int(position[cube][j]) * int(wallNegRotacion[wallID][j][1])

				if newPos == 1:
					ConditionUpdated.add("back")
				elif newPos == -1:
					ConditionUpdated.add("front")
				elif newPos == 0:
					ConditionUpdated.add("standing")
				newPosY = newPos

				# koordinat dari Z
				newPos = 0
				if not negRotacion:
					for j in range(3):
						newPos = newPos + int(position[cube][j]) * int(wallRotacion[wallID][j][2])
				else:
					for j in range(3):
						newPos = newPos + int(position[cube][j]) * int(wallNegRotacion[wallID][j][2])

				if newPos == 1:
					ConditionUpdated.add("up")
				elif newPos == -1:
					ConditionUpdated.add("down")
				elif newPos == 0:
					ConditionUpdated.add("equator")
				newPosZ = newPos

				position[cube] = [newPosX, newPosY, newPosZ]

				for antWallID in ConditionAnterior - ConditionUpdated:
					walls[antWallID].remove(cube)
				for actWallID in ConditionUpdated - ConditionAnterior:
					walls[actWallID].append(cube)

		self.sec = Sequence()




		def movement(wallID, negRotacion=False):
			self.sec.append(Func(reparentcubes, wallID))
			rot = rotaciones[wallID]["hpr"]
			if negRotacion:
				rot = rot * -1.
			#Menentukan Kecepatan Rotasi
			self.sec.append(LerpHprInterval(pivotes[wallID], 0.5, rot))
			self.sec.append(Func(UpdatedConditioncube, wallID, negRotacion))

		def acceptInputInput(): 
			# tambahkan rotasi positif "Depan"
			self.accept("f", lambda: movement("front"))
			# <Shift + F> menambahkan rotasi negatif "depan
			self.accept("shift-f", lambda: movement("front", True))
			# <B> tambahkan rotasi positif "kembali"
			self.accept("b", lambda: movement("back"))
			# <Shift + B> rotasi negatif gregra "kembali"
			self.accept("shift-b", lambda: movement("back", True))

			# <L> tambahkan rotasi positif "kiri"
			self.accept("l", lambda: movement("left"))
			# <Shift + L> menambahkan rotasi negatif "kiri"
			self.accept("shift-l", lambda: movement("left", True))
			# <R> tambahkan rotasi positif "kanan"
			self.accept("r", lambda: movement("right"))
			# <Shift + R> menambahkan rotasi negatif "kanan"
			self.accept("shift-r", lambda: movement("right", True))
			# <D> agrega rotacion positiva "down"
			self.accept("d", lambda: movement("down"))
			# <Shift+D> agrega rotacion negativa "down"
			self.accept("shift-d", lambda: movement("down", True))
			# <U> menambahkan rotasi Naik positif
			self.accept("u", lambda: movement("up"))
			# <Shift + U> menambahkan rotasi Naik negatif
			self.accept("shift-u", lambda: movement("up", True))

			# untuk memutar irisan tengah
			
			# <C> menambahkan rotasi balik positif
			self.accept("c", lambda: movement("center"))
			# <Shift + C> menambahkan rotasi mundur negatif
			self.accept("shift-c", lambda: movement("center", True))
			# untuk memutar irisan ekuator
			# <E> menambahkan rotasi Kembali positif
			self.accept("e", lambda: movement("equator"))
			# <Shift + E> menambahkan rotasi mundur negatif
			self.accept("shift-e", lambda: movement("equator", True))
			# untuk memutar irisan tegak
			# <S> menambahkan rotasi balik positif
			self.accept("s", lambda: movement("standing"))
			# <Shift+S> adds a negative Back rotation
			self.accept("shift-s", lambda: movement("standing", True))

			# <Enter> Mulai urutannya
			self.accept("enter", startSec)

		

		def ignoreInput():
			self.ignore("f")
			self.ignore("shift-f")
			self.ignore("b")
			self.ignore("shift-b")
			self.ignore("l")
			self.ignore("shift-l")
			self.ignore("r")
			self.ignore("shift-r")
			self.ignore("d")
			self.ignore("shift-d")
			self.ignore("u")
			self.ignore("shift-u")
			self.ignore("enter")

		def startSec():
			# Jangan izinkan input urutan selama urutan utama
			ignoreInput()
			# ... terima input input saat urutan berakhir
			self.sec.append(Func(acceptInputInput))
			self.sec.start()
			# Buat urutan baru, jadi tidak ada interval baru yang akan ditambahkan ke yang dimulai
			self.sec = Sequence()

		acceptInputInput()

		self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")	

		#Setel ulang fungsi tampilan kubus 
		def reset():
			self.trackball.node().setHpr(0, 0, 0)
		#Cube fungsi tampilan terbalik
		def reverse():
			self.trackball.node().setHpr(180, 0, 0)
		
		# Menekan "k" memulai kembali tampilan
		self.accept("k",reset)
		# Menekan "z" akan undo tampilan
		self.accept("z",reverse)

	#Fungsi yang memperbaiki kamera pada posisinya
	def spinCameraTask(self, task):
		self.camera.setPos(0,0,0)
		return Task.cont
		
	#Memuat Fungsi Layar
	def loadscreen(self):
		loadingText=OnscreenText("Simulator Rubik",1,fg=(1,1,1,1),pos=(0,0),align=TextNode.ACenter,scale=.07,mayChange=1)
		self.graphicsEngine.renderFrame() #render bingkai jika tidak, layar akan tetap hitam
		self.graphicsEngine.renderFrame() 
		self.graphicsEngine.renderFrame() 
		self.graphicsEngine.renderFrame()


        



app = MyApp()
# load Musik
mySound=app.loader.loadSfx("watatsumi.mp3")
# pemutar Musik
mySound.play()
# Membuat Musik terus berulang
mySound.setLoop(True)
# Mengatur volume
mySound.setVolume(15)
app.cam.node().getDisplayRegion(0).setSort(20)
render.setShaderAuto()
app.run()

