import datetime

test_cases = [
    {
        "input_data": {
			"metadata_date": datetime.datetime(2024, 4, 18, 0, 0, 0), 
			"raw_screen_text": ['Oconcept 2', 'PM5', 'View Detail', '5x6:00/2:00r.', 'Total Time:', 'Apr 18 2024.', '40:00.0', 'time meter', '1500m', '30:00.0', '8482.', '1:46.1 21', '6:00.0', '1627', '1:50.6 20 150', '6:00.0', '1677 1:47.3 21 161', '6:00.0', '1736', '1:43.6 23 169', '6:00.0', '1718. 1:44.7 22 171', '6:00.0', '1723 1:44.4 22 180', 'r245', 'Units', 'Display', 'Menu']
		},
        "expected_output": {
			"monitor_model": "PM5",
			"date": "2024-04-18",
			"session_name": "5x6:00/2:00r",
			"total_time": "00:40:00.0",
			"row_time": "00:30:00.0",
			"meters": "8482",
			"average_split": "1:46.1",
			"average_rate": "21",
			"intervals": [
				{
					"duration": "00:06:00.0",
					"meters": 1627,
					"split_time": "1:50.6",
					"stroke_rate": 20,
					"heart_rate": 150
				},
				{
					"duration": "00:06:00.0",
					"meters": 1677,
					"split_time": "1:47.3",
					"stroke_rate": 21,
					"heart_rate": 161
				},
				{
					"duration": "00:06:00.0",
					"meters": 1736,
					"split_time": "1:43.6",
					"stroke_rate": 23,
					"heart_rate": 169
				},
				{
					"duration": "00:06:00.0",
					"meters": 1718,
					"split_time": "1:44.7",
					"stroke_rate": 22,
					"heart_rate": 171
				},
				{
					"duration": "00:06:00.0",
					"meters": 1723,
					"split_time": "1:44.4",
					"stroke_rate": 22,
					"heart_rate": 180
				}
			]
		}
    },
    {
        "input_data": {
			"metadata_date": datetime.datetime(2015, 12, 17, 0, 0, 0), 
			"raw_screen_text": ['Oconcept 2', 'PM4', 'ROWING', 'View Detail', '2000m', 'Dec. 17 2015', 'time meter', '1500m /m', '6:32.3', '2000 1:38.0 32', '1:14.0', '400 1:32.5 33', '1:18.7', '.800 1:38.3 31', '1:20.7', '1200 1:40.8 31', '1:21.0', '1600 1:41.2 33', '1:17.9', '2000 1:37.3 :35', 'CHANGE', 'UNITS', 'CHANGE', 'DISPLAY', 'MENU', 'BACK'],
		},
		"expected_output": {
			"monitor_model": "PM4",
			"date": "2015-12-17",
			"session_name": "2000m",
			"total_time": "00:06:32.3",
			"row_time": "00:06:32.3",
			"meters": "2000",
			"average_split": "1:38.0",
			"average_rate": "32",
			"intervals": [
				{
					"duration": "00:01:14.0",
					"meters": 400,
					"split_time": "1:32.5",
					"stroke_rate": 33,
					"heart_rate": None
				},
				{
					"duration": "00:01:18.7",
					"meters": 800,
					"split_time": "1:38.3",
					"stroke_rate": 31,
					"heart_rate": None
				},
				{
					"duration": "00:01:20.7",
					"meters": 1200,
					"split_time": "1:40.8",
					"stroke_rate": 31,
					"heart_rate": None
				},
				{
					"duration": "00:01:21.0",
					"meters": 1600,
					"split_time": "1:41.2",
					"stroke_rate": 33,
					"heart_rate": None
				},
				{
					"duration": "00:01:17.9",
					"meters": 2000,
					"split_time": "1:37.3",
					"stroke_rate": 35,
					"heart_rate": None
				}
			]
		}
    },
    {
        "input_data": {
			"metadata_date": datetime.datetime(2019, 2, 14, 0, 0, 0), 
			"raw_screen_text": ['OKconcept 2', 'PM5', 'View Detail', '3x6000m/2:00r', 'Total Time:', 'Feb 14 2019', '1:13:23.7', 'time meter', '1500m', '1:07:23.7', '18000', '1:52.3 20', '22:29.6', '6000', '1:52.4 20', '22:28.5', '6000', '1:52.3 20', '22:25.6', '6000', '1:52.1 20', 'F108', 'Units', 'Display', 'Menu'],
		},
		"expected_output": {
			"monitor_model": "PM5",
			"date": "2019-02-14",
			"session_name": "3x6000m/2:00r",
			"total_time": "00:13:23.7",
			"row_time": "00:07:23.7",
			"meters": "18000",
			"average_split": "1:52.3",
			"average_rate": "20",
			"intervals": [
				{
					"duration": "00:22:29.6",
					"meters": 6000,
					"split_time": "1:52.4",
					"stroke_rate": 20,
					"heart_rate": None
				},
				{
					"duration": "00:22:28.5",
					"meters": 6000,
					"split_time": "1:52.3",
					"stroke_rate": 20,
					"heart_rate": None
				},
				{
					"duration": "00:22:25.6",
					"meters": 6000,
					"split_time": "1:52.1",
					"stroke_rate": 20,
					"heart_rate": None
				}
			]
		}
    },
    {
        "input_data": {
			"metadata_date": datetime.datetime(2019, 1, 7, 0, 0, 0), 
			"raw_screen_text": ['Iconcept 2.', 'PM4', 'diewy Detail', '15:00', 'Jan 07 2019', 'time meter 1500m', 'Pm', '15:00.0', '4292 1:44.8 20 173', '3:00.0', '849 1:46.0 20 164', '6:00.0', '854 1:45.3 20 172', '9:00.0', '851 1:45.7 20 173', '12:00.0', '855 1:45.2 20 178', '15:00.0', '882 1:42.0 21 182', 'CHANGE', 'CHANGE', 'MENU', 'UNITS', 'DISPLAY', 'BACK'],
		},
		"expected_output": {
			"monitor_model": "PM4",
			"date": "2019-01-07",
			"session_name": "15:00",
			"total_time": "00:15:00.0",
			"row_time": "00:15:00.0",
			"meters": "4292",
			"average_split": "1:44.8",
			"average_rate": "20",
			"intervals": [
				{
					"duration": "00:03:00.0",
					"meters": 849,
					"split_time": "1:46.0",
					"stroke_rate": 20,
					"heart_rate": 164
				},
				{
					"duration": "00:06:00.0",
					"meters": 854,
					"split_time": "1:45.3",
					"stroke_rate": 20,
					"heart_rate": 172
				},
				{
					"duration": "00:09:00.0",
					"meters": 851,
					"split_time": "1:45.7",
					"stroke_rate": 20,
					"heart_rate": 173
				},
				{
					"duration": "00:12:00.0",
					"meters": 855,
					"split_time": "1:45.2",
					"stroke_rate": 20,
					"heart_rate": 178
				},
				{
					"duration": "00:15:00.0",
					"meters": 882,
					"split_time": "1:42.0",
					"stroke_rate": 21,
					"heart_rate": 182
				}
			]
		}
    },
	{
		"input_data": {
			"metadata_date": datetime.datetime(2018, 9, 17, 9, 48, 9), 
			"raw_screen_text": ['OConcept 2', 'PM4', 'ROWING', 'Total Time:', '23:01.4', 'ume meter', '1500m /m', '30:01.4', '8000 1:52.5 18', '15:03.1', '4000 1:52.8 18', '14:58.3', '4000 1:52.2 18', 'r59', 'CHANGE', 'CHANGE', 'MENU', 'UNITS', 'DISPLAY', 'BACK'],
		},
		"expected_output": {
			"monitor_model": "PM4",
			"date": "2018-09-17",
			"session_name": "2x4000m/1:30r",
			"total_time": "00:33:01.4",
			"row_time": "00:30:01.4",
			"meters": "8000",
			"average_split": "1:52.5",
			"average_rate": "18",
			"intervals": [
				{
					"duration": "00:15:03.1",
					"meters": 4000,
					"split_time": "1:52.8",
					"stroke_rate": 18,
					"heart_rate": None
				},
				{
					"duration": "00:14:58.3",
					"meters": 4000,
					"split_time": "1:52.2",
					"stroke_rate": 18,
					"heart_rate": None
				}
			]
		}
	}
]