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
		GROUP
		{
			COLUMNS 2;
			LONG UVOL_Info_VolumeCount { ANIM OFF; }
			LONG UVOL_Info_VoxelCount { ANIM OFF; }
		}

		SEPARATOR { LINE; }
		
		VECTOR UVOL_BoundsSize { ANIM OFF; }
		VECTOR UVOL_CellsCount { ANIM OFF; }
		LONG UVOL_CellsSample
		{
			ANIM OFF;
			CYCLE
			{
				UVOL_CellsSample_Center;
				UVOL_CellsSample_Edges;
			}
		}
		BOOL UVOL_DrawPoints { ANIM OFF; }

		SEPARATOR { LINE; }
		
		BOOL UVOL_AutoGenerate  { ANIM OFF; }
		
		GROUP
		{
			COLUMNS 2;
			BUTTON UVOL_Button_GenerateSDF {}
			BUTTON UVOL_Button_ExportSDF {}
		}
		
		SEPARATOR { LINE; }
		
		GROUP
		{
			COLUMNS 2;
			BUTTON UVOL_Button_GenerateVF {}
			BUTTON UVOL_Button_ExportVF {}
		}
	}
}
