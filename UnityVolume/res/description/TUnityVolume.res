CONTAINER TUnityVolume
{
	NAME TUnityVolume;
    INCLUDE Texpression;
    
    GROUP ID_TAGPROPERTIES
	{
		LINK UNITY_VOLUME_Volume
		{
			ACCEPT { Ovolume; Ovolumebuilder; }
		}
		
		VECTOR UNITY_VOLUME_VolumeSize {}
		LONG UNITY_VOLUME_VolumeCount {}
		LONG UNITY_VOLUME_VoxelCount {}

		SEPARATOR { LINE; }
		
		GROUP
		{
			COLUMNS 2;
			BUTTON UNITY_VOLUME_ExportSDF {}
			BUTTON UNITY_VOLUME_ExportVF {}
		}
	}
}
