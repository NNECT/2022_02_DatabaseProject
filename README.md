기후데이터 시작화 웹 어플리케이션
===
_2022년 2학기 데이터베이스 프로젝트_

## 1. 개발환경
- Python (3.9)
- Flask (2.1.3)
- Bootstrap (5.2.2)

## 2. 개발목표
- 필요한 정보를 입력받고, 해당 정보에 맞는 데이터를 테이블 또는 그래프로 출력한다.
  - 기후 데이터를 입력받아 데이터베이스를 구축한다.
  - 데이터베이스 업데이트의 편의성을 추구한다.
  - 원하는 데이터를 선택하여 테이블 또는 그래프로 출력받고, 결과물을 다운로드 받을 수 있도록 한다.

## 3. 프로젝트 구성
- 프레젠테이션 [링크](https://docs.google.com/presentation/d/e/2PACX-1vTjri26MZu_JHAn6jReJZtX3LAD6IERa0nxameleXvdLV7qqpQnlrmtkD6IvRnzpA/pub?start=false&loop=false&delayms=10000)

### 3.1. 기능 구현
- 지정 폴더에 저장된 CSV 파일을 읽고 데이터베이스 업데이트 (기상자료개방포털에서 다운로드한 CSV 파일)
- 사용자가 원하는 날짜, 지역, 데이터 종류에 따라 테이블 또는 그래프 형태로 출력
- 출력된 테이블 / 그래프를 CSV / PNG 파일 형태로 다운로드

### 3.2. 데이터베이스
- location
  >- <u>location_id</u>: Integer
  >- location_name: String(10)
- climate_year
  >- <u>location_id</u>: Integer (Foreign Key → location.location_id)
  >- <u>chk_date</u>: String(4)
  >- tavg: Float
  >- tmin: Float
  >- tmax: Float
  >- rain_total: Float
  >- rain_max: Float
  >- humid_avg: Float
  >- wind_avg: Float
  >- light_time: Float
- climate_month
  >- <u>location_id</u>: Integer (Foreign Key → location.location_id)
  >- <u>chk_date</u>: String(7)
  >- tavg: Float
  >- tmin: Float
  >- tmax: Float
  >- rain_total: Float
  >- rain_max: Float
  >- humid_avg: Float
  >- wind_avg: Float
  >- wind_max: Float
  >- light_time: Float
- climate_day
  >- <u>location_id</u>: Integer (Foreign Key → location.location_id)
  >- <u>chk_date</u>: String(10)
  >- tavg: Float
  >- tmin: Float
  >- tmax: Float
  >- rain: Float
  >- humid_avg: Float
  >- wind_avg: Float
  >- wind_max: Float
  >- light_time: Float

### 3.3. 파일 구성
- climate_visualization.py
  > 프로젝트의 메인 파일<br>
  > url에 따른 처리 함수가 들어있다.<br>
  >- page_main
  >  > 앱 메인페이지<br> 해당 앱에서 어떤 작업을 할 것인지 선택한다(index.html).
  >- table
  >  > 테이블 페이지<br> 데이터가 전송되었으면 테이블을 출력(table.html),<br> 아니라면 데이터를 선택하는 페이지를 출력한다(s_table.html).
  >- graph
  >  > 그래프 페이지<br> 데이터가 전송되었으면 그래프를 출력(graph.html),<br> 아니라면 메인페이지에서 선택한 방식의 데이터 선택 페이지를 출력한다(s_graph.html, v_graph.html).
- models.py
  > 데이터베이스 초기화 파일<br>
  > 데이터베이스 초기 설정, 경로 설정 및 테이블 정의가 들어있다.
- db_update.py
  > 데이터베이스 업데이트 파일<br>
  > 홈페이지가 구동될 때, 새로운 데이터 CSV파일이 있는지 확인하여 데이터베이스를 업데이트한다.
  >- db_init
  >  > 데이터베이스 존재 여부를 확인하고, 있을 경우 업데이트, 없을 경우 새 데이터베이스 구축을 시행한다.
  >- db_update
  >  > 새로운 CSV파일이 있는지 확인하고, 각 파일에 대해 데이터베이스화 함수를 시행한다.
  >- file_to_db
  >  > 파일의 데이터를 읽어들여 데이터베이스에 추가 혹은 덮어쓰기를 시행한다.
- db_load.py
  > 필요한 데이터를 데이터베이스에서 읽어들이는 함수 파일
  >- db_load
  >  > (데이터 종류, 지역, 시간 단위, 시작 시간, 종료 시간)의 정보를 받고 해당하는 데이터를 출력한다.
- templates
  - layout.html
    > 페이지 레이아웃<br> 기본적인 head, js, css, navbar 정보가 들어있다.
  - index.html
    > 메인 페이지
  - s_table.html
    > 테이블 데이터 선택 페이지<br> 선택된 데이터를 table함수에 전달한다.
  - table.html
    > 테이블 페이지<br> 데이터를 테이블 형태로 출력한다.<br> 해당 테이블을 CSV파일로 저장할 수 있다.
  - s_graph.html
    > 단일지역 그래프 데이터 선택 페이지<br> 단일 지역에 대해 여러 데이터를 선택할 수 있다.<br> 선택된 데이터를 graph함수에 전달한다.
  - v_graph.html
    > 지역비교 그래프 데이터 선택 페이지<br> 단일 종류 데이터에 대해 여러 지역을 선택할 수 있다.<br> 선택된 데이터를 graph함수에 전달한다.
  - graph.html
    > 그래프 페이지<br> 데이터를 그래프 형태로 출력한다.<br> 해당 그래프를 이미지로 저장할 수 있다.
- static
  - selection_func.js
    > 선택 페이지에서 연간/월간/일간에 따라 다른 데이터 종류를 선택할 수 있도록 하는 자바스크립트 함수
  - download_table.js
    > 테이블 페이지에서 테이블을 CSV파일로 저장하도록 하는 자바스크립트 함수
  - download_graph.js
    > 그래프 페이지에서 그래프를 이미지로 저장하도록 하는 자바스크립트 함수
