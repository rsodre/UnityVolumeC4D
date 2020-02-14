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
		data.SetVector( c4d.UNITY_VOLUME_VolumeSize, c4d.Vector(0) )
		data.SetInt32( c4d.UNITY_VOLUME_VolumeCount, 0 )
		data.SetInt32( c4d.UNITY_VOLUME_VoxelCount, 0 )
		return True

	def GetDEnabling(self, node, id, t_data, flags, itemdesc):
		#data = node.GetDataInstance()
		#if data is None: return
		paramId = id[0].id
		if paramId == c4d.UNITY_VOLUME_Volume:
			return False
		if paramId == c4d.UNITY_VOLUME_VoxelCount:
			return False
		if paramId == c4d.UNITY_VOLUME_VolumeSize:
			return False
		if paramId == c4d.UNITY_VOLUME_VolumeCount:
			return False
		#elif id[0].id==c4d.SPLINEOBJECT_ANGLE:
		#	return inter==c4d.SPLINEOBJECT_INTERPOLATION_ADAPTIVE or inter==c4d.SPLINEOBJECT_INTERPOLATION_SUBDIV
		return True

	def GetDParameter(self, node, id, flags):
		paramId = id[0].id
		if paramId == c4d.UNITY_VOLUME_Volume:
			data = self.get_volume_link(node)
			return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		if paramId == c4d.UNITY_VOLUME_VolumeSize:
			vob = self.get_volume_object(node)
			if vob == None: return False
			volume = vob.GetVolume()
			dim = volume.GetActiveVoxelDim()
			data = c4d.Vector(dim.x,dim.y,dim.z)
			return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		if paramId == c4d.UNITY_VOLUME_VolumeCount:
			vob = self.get_volume_object(node)
			if vob == None: return False
			volume = vob.GetVolume()
			dim = volume.GetActiveVoxelDim()
			data = dim.x * dim.y * dim.z
			return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		if paramId == c4d.UNITY_VOLUME_VoxelCount:
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
			if commandId == c4d.UNITY_VOLUME_ExportSDF:
				self.export_sdf(node)
			if commandId == c4d.UNITY_VOLUME_ExportVF:
				print "Export VF"
		return True


	def export_sdf(self, node):
		print "Export SDF..."
		vob = self.get_volume_object(node)
		if vob == None: return False
		volume = vob.GetVolume()
		dim = volume.GetActiveVoxelDim()
		access = v.GridAccessorInterface.Create(maxon.Float32)
		access.Init(volume)
		'''
		for x in range(0, dim.x):
			for y in range(0, dim.y):
				for z in range(0, dim.z):
					coords = c4d.Vector(x, y, z)
					state = access.GetActiveState(coords)
					value = access.GetValue(coords)
					print " Data(%d,%d,%d) = [%d] %f" % (x,y,z,state,value)
		'''
		for x in range(0, 3):
			for y in range(0, 3):
				for z in range(0, 3):
					coords = c4d.Vector(-100+100*x, -100+100*y, -100+100*z)
					state = access.GetActiveState(coords)
					value = access.GetValue(coords)
					print " Data(%d,%d,%d) = [%d] %f" % (x,y,z,state,value)
		gridName = volume.GetGridName()
		print(gridName)
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
