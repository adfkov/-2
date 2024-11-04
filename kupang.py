import datetime
import random
import re

# 주문 클래스
class Order:
    def __init__(self, order_id, product_id, product_name, product_price, quantity, customer_name, customer_address, order_date):
        self.order_id = order_id
        self.product_id = product_id
        self.product_name = product_name
        self.product_price = product_price
        self.quantity = quantity
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.order_date = order_date

    def __str__(self):
        return (f"주문번호: {self.order_id}, 상품번호: {self.product_id}, 상품명: {self.product_name}, 가격: {self.product_price}원, "
                f"수량: {self.quantity}, 고객명: {self.customer_name}, 주소: {self.customer_address}, "
                f"주문일: {self.order_date}")

    def to_file_string(self):
        return (f"{self.order_id},{self.product_id},{self.product_name},{self.product_price},{self.quantity},"
                f"{self.customer_name},{self.customer_address},{self.order_date}\n")

    @staticmethod
    def from_file_string(order_str):
        order_data = order_str.strip().split(',')
        return Order(order_data[0], order_data[1], order_data[2], int(order_data[3]), int(order_data[4]), 
                     order_data[5], order_data[6], order_data[7])  # Add order_date as well

# 쇼핑몰 클래스
class ShoppingMall:
    def __init__(self):
        self.orders = []  # 주문 목록
        self.products = {}  # 상품 목록 (상품명: (가격, 수량))
        self.current_date = None
        self.load_items()
        self.load_orders()
        self.last_order_date = None  # 마지막 주문 날짜

    # 현재 날짜 설정
    def set_date(self):
        while True:
            try:
                input_date = input("현재 날짜를 입력하세요 (YYYY-MM-DD) 또는 '0'을 눌러 종료: ")
                if input_date == '0':
                    print("프로그램을 종료합니다.")
                    exit()
                year, month, day = map(int, input_date.split('-'))
                self.current_date = datetime.date(year, month, day)
                break
            except ValueError:
                print("잘못된 형식입니다. 다시 입력하세요.")

    def add_product(self):
        product_name = input("추가할 상품명: ")
        
        # 상품명 유효성 검사
        if not self.is_valid_product_name(product_name):
            print("상품명에는 적어도 하나 이상의 한글 또는 영어 문자가 포함되어야 합니다.")
            return

        while True:
            try:
                product_price = int(input("상품 가격 (정수로 입력): "))
                product_quantity = int(input("상품 수량 (정수로 입력): "))
                
                # 고유 상품 ID 생성
                product_id = f"PROD{random.randint(1000, 9999)}"
                
                # 상품 등록
                self.products[product_id] = (product_name, product_price, product_quantity)
                print(f"상품 '{product_name}', '{product_id}' 이(가) 추가되었습니다.")
                
                # 상품 파일 저장 (comment out this line temporarily for testing)
                self.save_items()
                break  # 루프 종료
                
            except ValueError as e:
                print(f"입력 오류: {e}. 가격과 수량은 정수만 입력 가능합니다. 다시 시도해주세요.")



    def is_valid_product_name(self, name):
        return bool(re.search("[A-Za-z가-힣]", name))  # 영어 또는 한글이 포함되어야 함

    def update_product(self, product_id):
        if product_id not in self.products:
            print(f"'{product_id}' 상품이 존재하지 않습니다.")
            return
        print(f"수정할 항목 선택: \n(1) 상품명\n(2) 가격\n(3) 수량")
        option = input("선택: ")
        if option == '1':
            new_name = input("새로운 상품명: ")
            
            # 상품명 유효성 검사
            if not self.is_valid_product_name(new_name):
                print("상품명에는 적어도 하나 이상의 한글 또는 영어 문자가 포함되어야 합니다.")
                return
            
            old_product = self.products.pop(product_id)
            self.products[product_id] = (new_name, old_product[1], old_product[2])
            print(f"'{old_product[0]}'의 이름이 '{new_name}'으로 변경되었습니다.")
        elif option == '2':
            while True:
                try:
                    new_price = int(input("새로운 가격 (정수로 입력): "))
                    old_product = self.products[product_id]
                    self.products[product_id] = (old_product[0], new_price, old_product[2])  # 가격만 변경
                    print(f"'{product_id}'의 가격이 '{new_price}'으로 변경되었습니다.")
                    break
                except ValueError:
                    print("가격은 정수만 입력 가능합니다. 다시 시도해주세요.")
        elif option == '3':
            while True:
                try:
                    new_quantity = int(input("새로운 수량 (정수로 입력): "))
                    old_product = self.products[product_id]
                    self.products[product_id] = (old_product[0], old_product[1], new_quantity)  # 수량만 변경
                    print(f"'{product_id}'의 수량이 '{new_quantity}'으로 변경되었습니다.")
                    break
                except ValueError:
                    print("수량은 정수만 입력 가능합니다. 다시 시도해주세요.")
        else:
            print("잘못된 입력입니다.")

    def remove_product(self):
        product_id = input("단종할 상품 ID: ")
        if product_id in self.products:
            del self.products[product_id]
            print(f"상품 ID '{product_id}'이(가) 삭제되었습니다.")
            self.save_items()
        else:
            print("해당 상품이 존재하지 않습니다.")


    # 상품 목록 조회
    def view_products(self):
        if not self.products:
            print("등록된 상품이 없습니다.")
        else:
            print(f"{'ID':<10} {'상품명':<20} {'가격':<10} {'수량':<10}")
            print("-" * 40)  # 구분선
        
            for product_id, (product_name, price, quantity) in self.products.items():
                print(f"{product_id:<10} {product_name:<20} {price:<10} {quantity:<10}")

    def search_products(self, query):
        # 검색어가 비어 있으면 빈 딕셔너리 반환
        if not query:
            print("검색어가 비어 있습니다.")
            return {}
        
        # 제품을 검색하여 결과를 딕셔너리로 반환
        results = {
            product_id: (name, price, quantity)
            for product_id, (name, price, quantity) in self.products.items()
            if query.lower() in name.lower()
        }
        
        return results

    # 관리자용 상품 관리
    def manage_products(self):
        while True:
            print("\n(1) 상품 조회\n(2) 상품 등록\n(3) 상품 수정\n(4) 단종 등록\n(0) 종료")
            choice = input("선택: ")
            if choice == '1':
                self.view_products()  # 상품 조회
            elif choice == '2':
                self.add_product()  # 상품 추가
            elif choice == '3':
                product_id = input("수정할 상품 ID를 입력하세요: ")
                self.update_product(product_id)  # 상품 수정
            elif choice == '4':
                self.remove_product()  # 상품 삭제
            elif choice == '0':
                print("상품 관리 화면을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다. 다시 선택하세요.")

   # 주문 추가 (고객용)
    def add_order(self):
        customer_name = input("고객 이름: ")
        customer_address = input("고객 주소: ")

        while True:  # 상품 선택을 위한 루프 추가
            search_query = input("상품명을 검색하세요 (입력을 원하지 않으면 '0'을 입력): ")
            if search_query == '0':
                print("검색을 종료합니다.")
                return  # 검색 종료

            print("검색 결과:")
            search_results = self.search_products(search_query)

            if not search_results:
                print("검색 결과가 없습니다. 다른 이름을 입력해보세요.")
            else:
                print(f"{'ID':<10} {'상품명':<20} {'가격':<10} {'수량':<10}")
                print("-" * 40)  # 구분선
                
                for product_id, (product_name, price, quantity) in search_results.items():
                    print(f"{product_id:<10} {product_name:<20} {price:<10} {quantity:<10}")

            # 상품 목록을 항상 표시
            print("상품 목록:")
            self.view_products()
            
            product_id = input("주문할 상품 ID를 입력하세요 (0을 입력하면 종료): ")
            if product_id == '0':
                print("주문을 종료합니다.")
                return  # 주문 종료

            if product_id in self.products:
                product_name, product_price, product_quantity = self.products[product_id]

                if product_quantity == 0:
                    print("주문 수량이 없어 주문이 불가합니다. 다른 상품을 선택하세요.")
                    continue  # 상품을 다시 선택하도록 루프의 시작으로 돌아감

                while True:
                    try:
                        quantity = int(input("주문할 수량 (0을 입력하면 종료): "))
                        if quantity == 0:
                            print("주문을 종료합니다.")
                            return  # 주문 종료
                        if quantity > product_quantity:
                            print("수량이 재고를 초과합니다.")
                            continue  # 수량이 적절하지 않으면 다시 입력받도록 함
                        break
                    except ValueError:
                        print("수량은 정수로 입력해주세요.")

                order_id = f"ORD{random.randint(1000, 9999)}"  # 고유 주문 ID 생성
                order_date = self.current_date or datetime.date.today()  # 현재 날짜가 없으면 오늘 날짜 사용
                order = Order(order_id, product_id, product_name, product_price, quantity, customer_name, customer_address, order_date)
                self.orders.append(order)

                # 상품 수량 업데이트
                new_quantity = product_quantity - quantity
                self.products[product_id] = (product_name, product_price, new_quantity)  # 수량 업데이트
                print(f"주문이 성공적으로 추가되었습니다: {order}")

                # 파일에 주문과 상품 정보 저장
                self.save_orders()
                self.save_items()  # 상품 정보도 함께 저장
                break  # 주문 추가 완료 후 루프 종료
            else:
                print("유효하지 않은 상품 ID입니다.")

    # 매출 정보 저장
    def save_sales(self, order):
        with open('sales.txt', 'a', encoding='utf-8') as f:
            total_price = order.product_price * order.quantity
            f.write(f"{order.product_name},{order.quantity},{total_price}원,{order.order_date}\n")

    # 주문 삭제 (관리자용)
    def remove_order(self):
        self.view_orders()
        order_id = input("삭제할 주문 번호: ")
        found = False
        for order in self.orders:
            if order.order_id == order_id:
                self.orders.remove(order)
                found = True
                print(f"주문 '{order_id}'이(가) 삭제되었습니다.")
                self.save_orders()
                break
        if not found:
            print("해당 주문이 존재하지 않습니다.")

   # 주문 목록 출력
    def view_orders(self):
        if not self.orders:
            print("등록된 주문이 없습니다.")
        else:
            # 헤더 출력
            print(f"{'주문번호':<12} {'상품번호':<10} {'상품명':<20} {'가격(원)':<10} {'수량':<8} {'고객명':<12} {'주소':<30} {'주문일':<15}")
            print("-" * 120)  # 구분선
            
            for order in self.orders:
                print(f"{order.order_id:<12} {order.product_id:<10} {order.product_name:<20} {order.product_price:<10} "
                      f"{order.quantity:<8} {order.customer_name:<12} {order.customer_address:<30} "
                      f"{order.order_date:<15}")


    # 매출 조회
    def view_sales(self):
        total_sales = 0
        print("\n매출 내역:")
        print(f"{'상품번호':<10} {'상품명':<10} {'수량':<10} {'총 가격':<10}")
        for order in self.orders:
            total_price = order.product_price * order.quantity
            print(f"{order.product_id:<10} {order.product_name:<10} {order.quantity:<10} {total_price:<10}원")
            total_sales += total_price
        print(f"총 매출액: {total_sales}원")

    # 파일로부터 상품 읽어오기
    def load_items(self):
        try:
            with open('products.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():  # Check if the line is not empty
                        product_id, product_name, product_price, product_quantity = line.strip().split(',')
                        self.products[product_id] = (product_name, int(product_price), int(product_quantity))  # 가격과 수량
        except FileNotFoundError:
            pass  # File not found, do nothing
        except ValueError:
            print("파일 형식이 잘못되었습니다. 상품 정보를 확인하세요.")  # Handle incorrect format

    def save_items(self):
        with open("products.txt", "w", encoding="utf-8") as file:
            for product_id, (name, price, quantity) in self.products.items():
                file.write(f"{product_id},{name},{price},{quantity}\n")

    # 파일로부터 주문 읽어오기
    def load_orders(self):
        try:
            with open('orders.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():  # Check if the line is not empty
                        order = Order.from_file_string(line)
                        self.orders.append(order)
        except FileNotFoundError:
            pass  # File not found, do nothing
        except ValueError:
            print("파일 형식이 잘못되었습니다. 주문 정보를 확인하세요.")  # Handle incorrect format

    # 주문 정보를 파일에 저장
    def save_orders(self):
        with open('orders.txt', 'w', encoding='utf-8') as f:
            for order in self.orders:
                f.write(order.to_file_string())

    # 고객 메뉴
    def customer_menu(self):
        while True:
            print("\n(1) 상품 목록 조회\n(2) 주문하기\n(0) 종료")
            choice = input("선택: ")
            if choice == '1':
                self.view_products()  # 상품 조회
            elif choice == '2':
                self.add_order()  # 주문하기
            elif choice == '0':
                print("고객 화면을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다. 다시 선택하세요.")

    # 관리자 메뉴
    def admin_menu(self):
        while True:
            print("\n(1) 상품 목록 조회\n(2) 주문 조회\n(3) 주문 삭제\n(4) 매출 조회\n(0) 종료")
            choice = input("선택: ")
            if choice == '1':
                self.manage_products()  # 상품 목록 및 관리
            elif choice == '2':
                self.view_orders()  # 주문 조회
            elif choice == '3':
                self.remove_order()  # 주문 삭제
            elif choice == '4':
                self.view_sales()  # 매출 조회
            elif choice == '0':
                print("관리자 화면을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다. 다시 선택하세요.")

    # 사용자 역할 선택
    def role_selection(self):
        while True:
            print("\n(1) 관리자 페이지\n(2) 고객 페이지\n(0) 종료")
            role = input("선택: ")
            if role == '2':
                self.customer_menu()  # 고객 메뉴로 이동
            elif role == '1':
                admin_code = input("관리자 코드를 입력하세요: ")
                if admin_code == "1234":  # 관리자 코드 수정
                    self.admin_menu()  # 관리자 메뉴로 이동
                else:
                    print("잘못된 관리자 코드입니다.")
                    continue  # 잘못된 코드일 경우 다시 시도하도록
            elif role == '0':
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다. 다시 선택하세요.")

# 프로그램 실행
if __name__ == "__main__":  
    shopping_mall = ShoppingMall()
    shopping_mall.role_selection()  # 역할 선택
