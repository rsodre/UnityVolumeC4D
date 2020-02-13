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

	def get_volume_builder(self, node):
		parent = node.GetObject()
		if parent != None and parent.CheckType(c4d.Ovolumebuilder):
			return parent
		return None
	
	def get_volume_object(self, node):
		builder = self.get_volume_builder(node)
		if builder != None:
			cache = builder.GetCache()
			if cache != None and cache.CheckType(c4d.Ovolume):
				return cache
		return None


	def Init(self, node):
		data = node.GetDataInstance()
		data.SetInt32( c4d.UNITY_VOLUME_VoxelCount, 0 )
		data.SetVector( c4d.UNITY_VOLUME_VoxelSize, c4d.Vector(0) )
		data.SetVector( c4d.UNITY_VOLUME_VolumeSize, c4d.Vector(0) )
		return True

	def GetDEnabling(self, node, id, t_data, flags, itemdesc):
		#data = node.GetDataInstance()
		#if data is None: return
		paramId = id[0].id
		if paramId == c4d.UNITY_VOLUME_Volume:
			return False
		if paramId == c4d.UNITY_VOLUME_VoxelCount:
			return False
		if paramId == c4d.UNITY_VOLUME_VoxelSize:
			return False
		if paramId == c4d.UNITY_VOLUME_VolumeSize:
			return False
		#elif id[0].id==c4d.SPLINEOBJECT_ANGLE:
		#	return inter==c4d.SPLINEOBJECT_INTERPOLATION_ADAPTIVE or inter==c4d.SPLINEOBJECT_INTERPOLATION_SUBDIV
		return True

	def GetDParameter(self, node, id, flags):
		paramId = id[0].id
		if paramId == c4d.UNITY_VOLUME_Volume:
			data = self.get_volume_builder(node)
			return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		if paramId == c4d.UNITY_VOLUME_VoxelCount:
			volume = self.get_volume_object(node)
			if volume == None: return False
			vi = volume.GetVolume()
			data = vi.GetActiveVoxelCount()
			return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		if paramId == c4d.UNITY_VOLUME_VoxelSize:
			volume = self.get_volume_object(node)
			if volume == None: return False
			itf = volume.GetVolume()
			dim = itf.GetActiveVoxelDim()
			data = c4d.Vector(dim.x,dim.y,dim.z)
			return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		if paramId == c4d.UNITY_VOLUME_VoxelSize:
			volume = self.get_volume_object(node)
			if volume == None: return False
			access = v.GridAccessorInterface.Create(maxon.Float32)
			access.Init(volume)
			#dim = vi.GetActiveVoxelDim()
			#data = c4d.Vector(dim.x,dim.y,dim.z)
			return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)
		return False

	def Message(self, node, type, data):
		if type == c4d.MSG_DESCRIPTION_COMMAND:
			if not data: return
			commandId = data['id'][0].id
			if commandId == c4d.UNITY_VOLUME_ExportSDF:
				print "Export SDF"
			if commandId == c4d.UNITY_VOLUME_ExportVF:
				print "Export VF"
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
