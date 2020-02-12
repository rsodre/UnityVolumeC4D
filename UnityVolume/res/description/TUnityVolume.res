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
		
		LONG UNITY_VOLUME_VolumeSize {}
		
		BUTTON UNITY_VOLUME_ExportSDF {}
		BUTTON UNITY_VOLUME_ExportVF {}
	}
}
