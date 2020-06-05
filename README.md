# ndds_json_2_yolo_txt
converting https://github.com/NVIDIA/Dataset_Synthesizer bounding box format (.json) into Yolo bbox format (.txt)

**JSON format image settings**
```
{
	"camera_data":
	{
		"location_worldframe": ,
		"quaternion_xyzw_worldframe":
	},
	"objects": [
		{
			"class": ,
			"instance_id":,
			"visibility": ,
			"location": ,
			"quaternion_xyzw":,
			"pose_transform": 
			],
			"cuboid_centroid": ,
			"projected_cuboid_centroid": ,
			"bounding_box":
			{
				"top_left": ,
				"bottom_right": 
			},
			"cuboid":
			],
			"projected_cuboid": 
		},
	]
}

```
