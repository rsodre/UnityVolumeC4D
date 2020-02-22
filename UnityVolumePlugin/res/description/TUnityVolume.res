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

		SEPARATOR { LINE; }
		
		LONG UVOL_DrawPoints
		{
			ANIM OFF;
			CYCLE
			{
				UVOL_DrawPoints_None;
				UVOL_DrawPoints_SDF;
				UVOL_DrawPoints_Gradient;
			}
		}
		
		LONG UVOL_PointSize
		{
			ANIM OFF;
			CUSTOMGUI LONGSLIDER;
			MIN 1;
			MAX 4;
		}


		BOOL UVOL_AutoGenerate  { ANIM OFF; }
		
		BUTTON UVOL_Button_GenerateSDF {}
		
		SEPARATOR { LINE; }
		
		FILENAME UVOL_ExportFilename
		{
			ANIM OFF;
			SAVE;
		}
				
		GROUP
		{
			COLUMNS 2;
			BUTTON UVOL_Button_ExportSDF {}
			BUTTON UVOL_Button_ExportGradient {}
		}
	}
}
