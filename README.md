# Quality Inspection Model for Lane Rendering

## Error Classes

| Assigned Code |        Class        |                   Description                    |                 Image                 |
| :-----------: | :-----------------: | :----------------------------------------------: | :-----------------------------------: |
|       0       |      No error       |        There are no errors in the images         | <img src="/error_types/0.png" width="50"> |
|       1       |  Center line error  | The road center line extends out of the juction. | ![error_1](/error_types/1.png =50x90) |
|       2       |   Stop line error   |     The stop line is in the middle of a road     | ![error_2](/error_types/2.png =50x90) |
|       3       | Guiding route error | The navigation route does not match actual road  | ![error_3](/error_types/3.png =50x90) |
|       4       | Road shoulder error |           The road shoulder is bumpy.            | ![error_4](/error_types/4.png =50x90) |
|       5       | Road surface error  |          A part of the road is missing.          | ![error_5](/error_types/5.png =50x90) |
|       6       |     Arrow error     |         The road marking arrows overlap.         | ![error_6](/error_types/6.png =50x90) |
|       7       |   Lane line error   |             The lane lines overlap.              | ![error_7](/error_types/7.png =50x90) |
