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

**JSON camera setting**
```
{
	"camera_settings": [
		{
			"name": "camera1",
			"horizontal_fov": 100,
			"intrinsic_settings":
			{
				"resX": 640,
				"resY": 480,
				"fx": 268.51190185546875,
				"fy": 268.51190185546875,
				"cx": 320,
				"cy": 240,
				"s": 0
			},
			"captured_image_size":
			{
				"width": 640,
				"height": 480
			}
		}
	]
}
```
