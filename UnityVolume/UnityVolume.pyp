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

# This ID is exclusive for this plugin, using the same will cause conflicts
# Get your own ID at Plugin Cafe, or use 1000001-1000010 for development
# http://www.plugincafe.com/forum/developer.asp
# com.studioavante.UnityVolume
PLUGIN_ID = 1054472

class UnityVolume(plugins.TagData):
	"""UnityVolume"""
	
	def Init(self, node):
		data = node.GetDataInstance()
		data.SetInt32( c4d.UNITY_VOLUME_VolumeSize, 1 )
		
		return True

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
