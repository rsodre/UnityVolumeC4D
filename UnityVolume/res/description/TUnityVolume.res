CONTAINER TUnityVolume
{
	NAME TUnityVolume;
    INCLUDE Texpression;
    
    GROUP ID_TAGPROPERTIES
	{
		LINK UVOL_Volume
		{
			ANIM OFF;
			ACCEPT { Ovolume; Ovolumebuilder; }
		}
		
		VECTOR UVOL_Info_VolumeSize { ANIM OFF; }
		LONG UVOL_Info_VolumeCount { ANIM OFF; }
		LONG UVOL_Info_VoxelCount { ANIM OFF; }

		SEPARATOR { LINE; }
		
		VECTOR UVOL_CellsCount { ANIM OFF; }
		VECTOR UVOL_BoundsSize { ANIM OFF; }
		BOOL UVOL_CellsCenter { ANIM OFF; }
		BOOL UVOL_DrawPoints { ANIM OFF; }

		SEPARATOR { LINE; }
		
		GROUP
		{
			COLUMNS 2;
			BUTTON UVOL_Button_ExportSDF {}
			BUTTON UVOL_Button_ExportVF {}
		}
	}
}
