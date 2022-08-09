# Quality Inspection Model for Lane Rendering

## Error Classes

| Assigned Code |        Class        |                   Description                    |                   Image                    |
| :-----------: | :-----------------: | :----------------------------------------------: | :----------------------------------------: |
|       0       |      No error       |        There are no errors in the images         | <img src="/error_types/0.png" width="100"> |
|       1       |  Center line error  | The road center line extends out of the juction. | <img src="/error_types/1.png" width="100"> |
|       2       |   Stop line error   |     The stop line is in the middle of a road     | <img src="/error_types/2.png" width="100"> |
|       3       | Guiding route error | The navigation route does not match actual road  | <img src="/error_types/3.png" width="100"> |
|       4       | Road shoulder error |           The road shoulder is bumpy.            | <img src="/error_types/4.png" width="100"> |
|       5       | Road surface error  |          A part of the road is missing.          | <img src="/error_types/5.png" width="100"> |
|       6       |     Arrow error     |         The road marking arrows overlap.         | <img src="/error_types/6.png" width="100"> |
|       7       |   Lane line error   |             The lane lines overlap.              | <img src="/error_types/7.png" width="100"> |
