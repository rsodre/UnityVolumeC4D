#
# UnityVolumeC4D
# Unity Volume tool for Cinema 4D
# Created by Roger Sodré, Feb 2020 @ Atibaia, Brazil
# https://github.com/rsodre/UnityVolumeC4D
#

import os
import math
from struct import *
import c4d
from c4d import bitmaps, plugins, utils
import maxon
from maxon.frameworks import volume as v

# This ID is exclusive for this plugin, using the same will cause conflicts
# Get your own ID at Plugin Cafe, or use 1000001-1000010 for development
# http://www.plugincafe.com/forum/developer.asp
# com.studioavante.UnityVolume
PLUGIN_ID = 1054472

class UnityVolume(plugins.TagData):
	"""UnityVolume"""

	size_ = []
	states_ = []
	values_ = []
	points_ = []
	colors_ = []
	gradients_ = []
	generated_ = False
	vobDirty_ = -1

	def get_volume_link(self, node):
		parent = node.GetObject()
		if parent == None: return None
		if parent.IsInstanceOf(c4d.Ovolume) or parent.IsInstanceOf(c4d.Ovolumebuilder):
			return parent
		return None
	
	def get_volume_object(self, node):
		parent = node.GetObject()
		if parent == None: return None
		if parent.IsInstanceOf(c4d.Ovolume):
			return parent
		if parent.IsInstanceOf(c4d.Ovolumebuilder):
			cache = parent.GetCache()
			if cache != None and cache.CheckType(c4d.Ovolume):
				return cache
		return None


	def Init(self, node):
		bc = node.GetDataInstance()
		bc.SetVector( c4d.UVOL_CellsCount, c4d.Vector(20,20,20) )
		bc.SetInt32( c4d.UVOL_CellsSample, c4d.UVOL_CellsSample_Center )
		bc.SetInt32( c4d.UVOL_DrawPoints, c4d.UVOL_DrawPoints_SDF )
		bc.SetInt32( c4d.UVOL_PointSize, 2)
		bc.SetBool( c4d.UVOL_AutoGenerate, True )
		bc.SetFilename( c4d.UVOL_ExportFilename, None )
		bc.SetVector( c4d.UVOL_BoundsSize, c4d.Vector(200,200,200) )
		bc.SetVector( c4d.UVOL_Info_VolumeSize, c4d.Vector(0) )
		bc.SetInt32( c4d.UVOL_Info_VolumeCount, 0 )
		bc.SetInt32( c4d.UVOL_Info_VoxelCount, 0 )
		return True

	def GetDEnabling(self, node, id, t_data, flags, itemdesc):
		#bc = node.GetDataInstance()
		#if data is None: return
		paramId = id[0].id
		if paramId == c4d.UVOL_Volume:
			return False
		if paramId == c4d.UVOL_Info_VoxelCount:
			return False
		if paramId == c4d.UVOL_Info_VolumeSize:
			return False
		if paramId == c4d.UVOL_Info_VolumeCount:
			return False
		return True

	def GetDParameter(self, node, id, flags):
		paramId = id[0].id
		if paramId == c4d.UVOL_Volume:
			data = self.get_volume_link(node)
			return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		if paramId == c4d.UVOL_Info_VolumeSize:
			vob = self.get_volume_object(node)
			if vob is not None:
				volume = vob.GetVolume()
				dim = volume.GetActiveVoxelDim()
				data = c4d.Vector(dim.x,dim.y,dim.z)
				return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		if paramId == c4d.UVOL_Info_VolumeCount:
			vob = self.get_volume_object(node)
			if vob is not None:
				volume = vob.GetVolume()
				dim = volume.GetActiveVoxelDim()
				data = dim.x * dim.y * dim.z
				return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		if paramId == c4d.UVOL_Info_VoxelCount:
			vob = self.get_volume_object(node)
			if vob is not None:
				volume = vob.GetVolume()
				data = volume.GetActiveVoxelCount()
				return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		return False

	def Message(self, node, type, data):
		if type == c4d.MSG_DESCRIPTION_COMMAND:
			if not data: return
			commandId = data['id'][0].id
			if commandId == c4d.UVOL_Button_GenerateSDF:
				self.generate_sdf(node)
			if commandId == c4d.UVOL_Button_ExportSDF:
				self.generate_sdf(node)
				self.export_vf(node, 'F', '_sdf')
			if commandId == c4d.UVOL_Button_ExportGradient:
				self.generate_sdf(node)
				self.export_vf(node, 'V', '_gradient')
		return True

	def CheckDirty(self, op, doc):
		vobDirty = -1
		vob = self.get_volume_object(tag)
		if vob is not None:
			vobDirty = vob.GetDirty(c4d.DIRTYFLAGS_DATA | c4d.DIRTYFLAGS_MATRIX | c4d.DIRTYFLAGS_CACHE)
		if self.vobDirty_ != vobDirty:
			op.SetDirty(c4d.DIRTYFLAGS_DATA)
			c4d.EventAdd()
			vobDirty_ = vobDirty

	def AddToExecution(self, tag, list):
		list.Add(tag, c4d.EXECUTIONPRIORITY_GENERATOR, 0)
		return True
	
	def Execute(self, tag, doc, op, bt, priority, flags):
		bc = tag.GetDataInstance()
		if bc.GetBool(c4d.UVOL_AutoGenerate):
			self.generate_sdf(tag)
		return c4d.EXECUTIONRESULT_OK

	#-----------------------------------------------------------
	# Draw
	#
	def Draw(self, node, op, bd, bh):
		vob = self.get_volume_object(node)
		#bd.SetMatrix_Matrix( vob, vob.GetMg() )
		bd.SetMatrix_Matrix( None, c4d.Matrix() )

		bc = node.GetDataInstance()
		bd.SetPointSize(bc.GetInt32(c4d.UVOL_PointSize))
		
		if bc.GetInt32(c4d.UVOL_DrawPoints) == c4d.UVOL_DrawPoints_SDF and len(self.points_) > 0 and len(self.colors_) > 0:
			bd.DrawPoints( self.points_, self.colors_, len(self.colors_)/len(self.points_) )
		if bc.GetInt32(c4d.UVOL_DrawPoints) == c4d.UVOL_DrawPoints_Gradient and len(self.points_) > 0 and len(self.gradients_) > 0:
			bd.DrawPoints( self.points_, self.gradients_, len(self.gradients_)/len(self.points_) )

		# Draws the overall bounding box
		#boundsColor = c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT);
		boundsColor = c4d.Vector(0,1,1) if self.generated_ else c4d.Vector(1,0,0)
		boundsSize = bc.GetVector(c4d.UVOL_BoundsSize)
		box = c4d.Matrix()
		box.v1 = box.v1 * (boundsSize.x * 0.5)
		box.v2 = box.v2 * (boundsSize.y * 0.5)
		box.v3 = box.v3 * (boundsSize.z * 0.5)
		bd.DrawBox(box, 1.0, boundsColor, True)
	
		return c4d.DRAWRESULT_OK
	

	#-----------------------------------------------------------
	# Generate SDF
	#
	def generate_sdf(self, node):
		self.generated_ = False
		
		vob = self.get_volume_object(node)
		if vob == None:
			return False
		volume = vob.GetVolume()
		access = v.GridAccessorInterface.Create(maxon.Float32)
		access.Init(volume)
		#print volume.GetGridName()
		#print volume.GetGridType()
		#print volume.GetGridTransform()

		# Create Gradient
		gradVolume = v.VolumeToolsInterface.CreateGradientVolume(volume, maxon.ThreadRef())
		gradAccess = v.GridAccessorInterface.Create(maxon.Vector32)
		gradAccess.Init(gradVolume)

		bc = node.GetDataInstance()
		cellsCount = bc.GetVector(c4d.UVOL_CellsCount)
		boundsSize = bc.GetVector(c4d.UVOL_BoundsSize)
		boundsMin = boundsSize * -0.5
		boundsMax = boundsSize * 0.5

		xrange = []
		yrange = []
		zrange = []
		cellsSize = c4d.Vector( boundsSize.x/cellsCount.x, boundsSize.y/cellsCount.y, boundsSize.z/cellsCount.z )
		if bc.GetInt32(c4d.UVOL_CellsSample) == c4d.UVOL_CellsSample_Center:
			volumeSize = [ int(cellsCount.x), int(cellsCount.y), int(cellsCount.z) ]
			for x in range( 0, volumeSize[0] ):
				xrange.append( boundsMin.x + (x + 0.5) * cellsSize.x )
			for y in range( 0, volumeSize[1] ):
				yrange.append( boundsMin.y + (y + 0.5) * cellsSize.y )
			for z in range( 0, volumeSize[2] ):
				zrange.append( boundsMin.z + (z + 0.5) * cellsSize.z )
		else:
			volumeSize = [ int(cellsCount.x)+1, int(cellsCount.y)+2, int(cellsCount.z)+3 ]
			for x in range( 0, volumeSize[0] ):
				xrange.append( boundsMin.x + x * cellsSize.x )
			for y in range( 0, volumeSize[1] ):
				yrange.append( boundsMin.y + y * cellsSize.y )
			for z in range( 0, volumeSize[2] ):
				zrange.append( boundsMin.z + z * cellsSize.z )

		coords = []
		states = []
		values = []
		grads = []
		valueMin = 0
		valueMax = 0
		for x in xrange:
			for y in yrange:
				for z in zrange:
					coord = c4d.Vector(x,y,z)
					state = access.GetActiveState(coord)
					value = access.GetValue(coord)
					grad = gradAccess.GetValue(coord)
					coords.append( coord )
					states.append( state )
					values.append( value )
					grads.append( grad )
					if value > 0 and value > valueMax:
						valueMax = value
					if value < 0 and value < valueMin:
						valueMin = value
					#print " Data(%d,%d,%d) = [%d] %f" % (x,y,z,state,value)

		#print "range %f > %f" % (valueMin,valueMax)
		#mv = max( abs(valueMin), valueMax )
		for i, val in enumerate(values):
			#values[i] = val / mv
			if val < 0:
				values[i] = val / abs(valueMin)
			else:
				values[i] = val / valueMax

		self.size_ = volumeSize
		self.states_ = states
		self.values_ = values
		self.points_ = coords
		self.gradients_ = []
		self.colors_ = []
		for grad in grads:
			self.gradients_.extend( [ grad.x, grad.y, grad.z ] )
		for val in values:
			if val < 0:
				self.colors_.extend( [ abs(val), abs(val), abs(val) ] )
			else:
				self.colors_.extend( [ 0, 0, value ] )

		#print "SDF Generated!"
		self.generated_ = True
		return True

	#-----------------------------------------------------------
	# Export
	#
	def export_vf(self, node, dataType, suffix=None):

		if dataType != 'F' and dataType != 'V':
			print "Invalid export data type [" + dataType + "]"
			return False
		if len(self.size_) != 3:
			print "Empty volume!"
			return False
		if self.size_[0] == 0 or self.size_[1] == 0 or self.size_[2] == 0 or self.size_[0] > 65535 or self.size_[1] > 65535 or self.size_[2] > 65535:
			print "Invalid volume size " + str(self.size_)
			return False

		print "Export VF [" + dataType + "]..."
		
		bc = node.GetDataInstance()
		filePath = str(bc.GetFilename(c4d.UVOL_ExportFilename))
		if not self.validate_filename(filePath):
			return False
		
		if suffix is not None:
			(root, ext) = os.path.splitext(filePath)
			filePath = root + suffix + ext

		# Open file
		fo = open(filePath, "wb")
		
		# vf file format
		# https://github.com/peeweek/VectorFieldFile
		# - FourCC (4 Bytes)
		#	"VF_F" for float field or "VF_V" fori Vector field
		fo.write("VF_")
		fo.write(dataType)
		# - Volume Size (6 Bytes)
		#	3 ushort describes the X,Y, & Z size of the volume, with a maximum of 65535
		#	pack() https://docs.python.org/2/library/struct.html
		data = pack('<HHH', self.size_[0], self.size_[1], self.size_[2] )
		fo.write(data)
		# - Data (size_X * size_Y * size_Z * Stride) where Stride = 1 (float) or 3 (vector)
		#	Float = 4 bytes
		#	Vector = 12 bytes
		if dataType == 'F':
			for val in self.values_:
				data = pack('f', val)
				fo.write(data)
		if dataType == 'V':
			for grad in self.gradients_:
				data = pack('f', grad)
				fo.write(data)

		# Close file
		fo.close()
		print "Exported [" + filePath + "]"
		return True

	
	#-----------------------------------------------------------
	# Misc
	#
	def validate_filename(self, filePath):
		fileFolder = os.path.dirname(filePath)
		fileExtension = os.path.splitext(filePath)[1].lower()
		if filePath is None or filePath == '':
			print "Filename not set"
			return False
		if fileFolder == '' or not os.path.exists(fileFolder) or not os.path.isdir(fileFolder):
			print "Filename has invalid folder"
			return False
		if fileExtension != '.vf':
			print "Filename extension must be [.vf]"
			return False
		return True




if __name__ == "__main__":
	bmp = bitmaps.BaseBitmap()
	dir, file = os.path.split(__file__)
	fn = os.path.join(dir, "res", "TUnityVolume.tif")
	bmp.InitWith(fn)
	plugins.RegisterTagPlugin(id=PLUGIN_ID,
							  str="UnityVolume",
							  info=c4d.TAG_EXPRESSION|c4d.TAG_VISIBLE,
							  g=UnityVolume,
							  description="TUnityVolume",
							  icon=bmp)
