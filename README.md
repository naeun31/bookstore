# bookstore
for Mr. vertigo bookstore

admin.py 참고하면 
db 의 테이블 shelf_num 컬럼을 그대로 쓰는형태로 했고
모든 조회는 elasticsearch 에서 가져오는것으로 변경
신규등록, 서가위치 추가 시 db 의 shelf_num 컬럼변경 작업 필요
elasticsearch 에서 작업한것과 동일하게 처리하면될듯.
