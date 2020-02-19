#
# UnityVolumeC4D
# Unity Volume tool for Cinema 4D
# Created by Roger Sodré, Feb 2020 @ Atibaia, Brazil
# https://github.com/rsodre/UnityVolumeC4D
#

import os
import math
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

	points_ = []
	colors_ = []

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
		data = node.GetDataInstance()
		data.SetVector( c4d.UVOL_CellsCount, c4d.Vector(20,20,20) )
		data.SetBool( c4d.UVOL_CellsCenter, True )
		data.SetBool( c4d.UVOL_DrawPoints, True )
		data.SetVector( c4d.UVOL_BoundsSize, c4d.Vector(200,200,200) )
		data.SetVector( c4d.UVOL_Info_VolumeSize, c4d.Vector(0) )
		data.SetInt32( c4d.UVOL_Info_VolumeCount, 0 )
		data.SetInt32( c4d.UVOL_Info_VoxelCount, 0 )
		return True

	def GetDEnabling(self, node, id, t_data, flags, itemdesc):
		#data = node.GetDataInstance()
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
		#elif id[0].id==c4d.SPLINEOBJECT_ANGLE:
		#	return inter==c4d.SPLINEOBJECT_INTERPOLATION_ADAPTIVE or inter==c4d.SPLINEOBJECT_INTERPOLATION_SUBDIV
		return True

	def GetDParameter(self, node, id, flags):
		paramId = id[0].id
		if paramId == c4d.UVOL_Volume:
			data = self.get_volume_link(node)
			return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		if paramId == c4d.UVOL_Info_VolumeSize:
			vob = self.get_volume_object(node)
			if vob == None: return False
			volume = vob.GetVolume()
			dim = volume.GetActiveVoxelDim()
			data = c4d.Vector(dim.x,dim.y,dim.z)
			return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		if paramId == c4d.UVOL_Info_VolumeCount:
			vob = self.get_volume_object(node)
			if vob == None: return False
			volume = vob.GetVolume()
			dim = volume.GetActiveVoxelDim()
			data = dim.x * dim.y * dim.z
			return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		if paramId == c4d.UVOL_Info_VoxelCount:
			vob = self.get_volume_object(node)
			if vob == None: return False
			volume = vob.GetVolume()
			data = volume.GetActiveVoxelCount()
			return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		return False

	def Message(self, node, type, data):
		if type == c4d.MSG_DESCRIPTION_COMMAND:
			if not data: return
			commandId = data['id'][0].id
			if commandId == c4d.UVOL_Button_ExportSDF:
				self.export_sdf(node)
			if commandId == c4d.UVOL_Button_ExportVF:
				print "Export VF"
		return True


	def export_sdf(self, node):
		print "Export SDF..."
		vob = self.get_volume_object(node)
		if vob == None: return False
		volume = vob.GetVolume()
		access = v.GridAccessorInterface.Create(maxon.Float32)
		access.Init(volume)
		#xform = volume.GetGridTransform()
		#gridName = volume.GetGridName()
		
		data = node.GetDataInstance()
		cellsCount = data.GetVector(c4d.UVOL_CellsCount)
		boundsSize = data.GetVector(c4d.UVOL_BoundsSize)
		boundsMin = boundsSize * -0.5
		boundsMax = boundsSize * 0.5

		xrange = []
		yrange = []
		zrange = []
		cellsSize = c4d.Vector( boundsSize.x/cellsCount.x, boundsSize.y/cellsCount.y, boundsSize.z/cellsCount.z )
		if data.GetBool(c4d.UVOL_CellsCenter):
			for x in range( 0, int(cellsCount.x) ):
				xrange.append( boundsMin.x + (x + 0.5) * cellsSize.x )
			for y in range( 0, int(cellsCount.y) ):
				yrange.append( boundsMin.y + (y + 0.5) * cellsSize.y )
			for z in range( 0, int(cellsCount.z) ):
				zrange.append( boundsMin.z + (z + 0.5) * cellsSize.z )
		else:
			for x in range( 0, int(cellsCount.x)+1 ):
				xrange.append( boundsMin.x + x * cellsSize.x )
			for y in range( 0, int(cellsCount.y)+1 ):
				yrange.append( boundsMin.y + y * cellsSize.y )
			for z in range( 0, int(cellsCount.z)+1 ):
				zrange.append( boundsMin.z + z * cellsSize.z )

		coords = []
		states = []
		values = []
		valueMin = 0
		valueMax = 0
		for x in xrange:
			for y in yrange:
				for z in zrange:
					coord = c4d.Vector(x,y,z)
					state = access.GetActiveState(coord)
					value = access.GetValue(coord)
					coords.append( coord )
					states.append( state )
					values.append( value )
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

		self.points_ = []
		self.colors_ = []
		if data.GetBool(c4d.UVOL_DrawPoints):
			for p in coords:
				self.points_.append( p )
			for val in values:
				#self.colors_.append( abs(val) )
				if val < 0:
					self.colors_.extend( [ abs(val), abs(val), abs(val) ] )
				else:
					self.colors_.extend( [ value, 0, 0 ] )
			#for st in states:
				#self.colors_.append( 1.0 if st else 0.0 )

		return True

	def Draw(self, node, op, bd, bh):
		bd.SetMatrix_Matrix( None, c4d.Matrix() )
		
		data = node.GetDataInstance()
		if data.GetBool(c4d.UVOL_DrawPoints) and len(self.points_) > 0 and len(self.colors_) > 0:
			bd.DrawPoints( self.points_, self.colors_, len(self.colors_)/len(self.points_) )

		# Draws the overall bounding box
		boundsSize = data.GetVector(c4d.UVOL_BoundsSize)
		box = c4d.Matrix()
		box.v1 = box.v1 * (boundsSize.x * 0.5)
		box.v2 = box.v2 * (boundsSize.y * 0.5)
		box.v3 = box.v3 * (boundsSize.z * 0.5)
		bd.DrawBox(box, 1.0, c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT), True)

		return c4d.DRAWRESULT_OK



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
