Dữ liệu của cuộc thi được cho tại aivivn_timeseries.

Cấu trúc của bộ dữ liệu như sau:

aivivn_timeseries]

```base
.
├── train.csv
├── test_id.csv
└── sample_submission.csv
```

## Dữ liệu huấn luyện

Dữ liệu huấn luyện (file train.csv) gồm hơn 6 triệu dòng. Dưới đây là năm dòng đầu tiên.

```
UPDATE_TIME,HOUR_ID,ZONE_CODE,SERVER_NAME,BANDWIDTH_TOTAL,MAX_USER
2017-10-01,0,ZONE01,SERVER_ZONE01_001,26.906931818181818,612.0
2017-10-01,0,ZONE01,SERVER_ZONE01_002,61.48169272727273,561.0
2017-10-01,0,ZONE01,SERVER_ZONE01_003,20.609837272727273,969.0
2017-10-01,0,ZONE01,SERVER_ZONE01_004,97.73738363636363,1377.0
2017-10-01,0,ZONE01,SERVER_ZONE01_005,113.25068454545455,1887.0
```

* UPDATE_TIME: ngày thực hiện lấy dữ liệu
* HOUR_ID: giờ thực hiện lấy dữ liệu
* ZONE_CODE: mã khu vực
* SERVER_NAME: tên của các server trong khu vực
* BAND_WIDTH_TOTAL: tổng băng thông truy cập tương ứng trong vòng 1 giờ
* MAX_USER: số user truy cập đồng thời tối đa trong vòng 1 giờ (là một số tự nhiên)

## Dữ liệu kiểm tra

Dữ liệu kiểm tra (file test.csv) bao gồm 390580 dòng có dạng:

```
id,UPDATE_TIME,HOUR_ID,ZONE_CODE,SERVER_NAME
0,2019-03-10,0,ZONE01,SERVER_ZONE01_001
1,2019-03-10,1,ZONE01,SERVER_ZONE01_001
2,2019-03-10,2,ZONE01,SERVER_ZONE01_001
```

Trong đó UPDATE_TIME, HOUR_ID, ZONE_CODE, SERVER_NAME được định nghĩa như trên, id là mã số tương ứng cho file nộp bài. Các đội chơi cần dự đoán BANDWIDTH_TOTAL, và MAX_USER cho mỗi dòng.

## Nộp bài

File nộp bài bắt buộc là một file .csv tương tự như file sample_submission.csv. Ví dụ:

```
id,label
0,35.74 271
1,0.77 143
```

**Chú ý**: giá trị thứ nhất trong label là BANDWIDTH_TOTAL được làm tròn hai chữ số thập phân, giá trị thứ hai là MAX_USER, là một số tự nhiên. Hai giá trị này cách nhau đúng một dấu khoảng trắng.
