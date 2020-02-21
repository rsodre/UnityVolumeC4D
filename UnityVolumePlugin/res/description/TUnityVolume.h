#ifndef _TUnityVolume_H_
#define _TUnityVolume_H_

enum
{
	UVOL_Volume = 1000,
	UVOL_CellsCount,
	UVOL_CellsSample,
	UVOL_BoundsSize,
	UVOL_DrawPoints,
	UVOL_AutoGenerate,
	UVOL_ExportFilename,

	UVOL_Info_VolumeSize = 1100,
	UVOL_Info_VolumeCount,
	UVOL_Info_VoxelCount,

	UVOL_Button_GenerateSDF = 1200,
	UVOL_Button_ExportSDF,
	UVOL_Button_GenerateVF,
	UVOL_Button_ExportVF
}

enum
{
	UVOL_CellsSample_Center,
	UVOL_CellsSample_Edges,
}

#endif