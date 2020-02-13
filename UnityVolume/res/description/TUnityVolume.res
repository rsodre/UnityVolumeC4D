CONTAINER TUnityVolume
{
	NAME TUnityVolume;
    INCLUDE Texpression;
    
    GROUP ID_TAGPROPERTIES
	{
		LINK UNITY_VOLUME_Volume
		{
			ACCEPT { Ovolumebuilder; }
		}
		
		VECTOR UNITY_VOLUME_VoxelSize {}
		LONG UNITY_VOLUME_VoxelCount {}
		VECTOR UNITY_VOLUME_VolumeSize {}

		SEPARATOR { LINE; }
		
		GROUP
		{
			COLUMNS 2;
			BUTTON UNITY_VOLUME_ExportSDF {}
			BUTTON UNITY_VOLUME_ExportVF {}
		}
	}
}
