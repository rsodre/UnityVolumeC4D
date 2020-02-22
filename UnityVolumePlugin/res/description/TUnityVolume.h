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
	UVOL_PointSize,

	UVOL_Info_VolumeSize = 1100,
	UVOL_Info_VolumeCount,
	UVOL_Info_VoxelCount,

	UVOL_Button_GenerateSDF = 1200,
	UVOL_Button_ExportSDF,
	UVOL_Button_ExportGradient
}

enum
{
	UVOL_CellsSample_Center,
	UVOL_CellsSample_Edges,
}

enum
{
	UVOL_DrawPoints_None,
	UVOL_DrawPoints_SDF,
	UVOL_DrawPoints_Gradient
}

#endif
