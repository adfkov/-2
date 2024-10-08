import datetime
import random
import re
# 주문 클래스
class Order:
    def __init__(self, order_id, product_name, product_price, quantity, customer_name, customer_address, order_date):
        self.order_id = order_id
        self.product_name = product_name
        self.product_price = product_price
        self.quantity = quantity
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.order_date = order_date

    def __str__(self):
        return (f"주문번호: {self.order_id}, 상품명: {self.product_name}, 가격: {self.product_price}원, "
                f"수량: {self.quantity}, 고객명: {self.customer_name}, 주소: {self.customer_address}, "
                f"주문일: {self.order_date}")

    def to_file_string(self):
        return (f"{self.order_id},{self.product_name},{self.product_price},{self.quantity},"
                f"{self.customer_name},{self.customer_address},{self.order_date}\n")

    @staticmethod
    def from_file_string(order_str):
        order_data = order_str.strip().split(',')
        return Order(order_data[0], order_data[1], int(order_data[2]), int(order_data[3]), 
                     order_data[4], order_data[5], order_data[6])


# 쇼핑몰 클래스
class ShoppingMall:
    def __init__(self):
        self.orders = []  # 주문 목록
        self.products = {}  # 상품 목록 (상품명: (가격, 수량))
        self.current_date = None
        self.load_items()
        self.load_orders()

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

    # 상품 추가
   
    # 상품 추가
    def add_product(self):
        product_name = input("추가할 상품명: ")
        
        # 상품명 유효성 검사
        if not self.is_valid_product_name(product_name):
            print("상품명에는 적어도 하나 이상의 한글 또는 영어 문자가 포함되어야 합니다.")
            return

        while True:
            try:
                product_price = int(input("상품 가격 (정수로 입력): "))  # 가격은 정수로 받습니다.
                product_quantity = int(input("상품 수량 (정수로 입력): "))  # 수량도 추가
                self.products[product_name] = (product_price, product_quantity)
                print(f"상품 '{product_name}'이(가) 추가되었습니다.")
                self.save_items()
                break
            except ValueError:
                print("가격과 수량은 정수만 입력 가능합니다. 다시 시도해주세요.")

    def is_valid_product_name(self, name):
        # 상품명에 적어도 하나 이상의 한글 또는 영어 문자가 포함되어 있는지 검사
        return bool(re.search("[A-Za-z가-힣]", name))  # 영어 또는 한글이 포함되어야 함

    # 나머지 메서드들은 동일하게 유지됩니다.

    # 상품 수정
    def update_product(self, product_name):
        if product_name not in self.products:
            print(f"'{product_name}' 상품이 존재하지 않습니다.")
            return
        print(f"수정할 항목 선택: \n1. 상품명\n2. 가격\n3. 수량")
        option = input("선택: ")
        if option == '1':
            new_name = input("새로운 상품명: ")
            
            # 상품명 유효성 검사
            if not self.is_valid_product_name(new_name):
                print("상품명에는 적어도 하나 이상의 한글 또는 영어 문자가 포함되어야 합니다.")
                return
            
            self.products[new_name] = self.products.pop(product_name)
            print(f"'{product_name}'의 이름이 '{new_name}'으로 변경되었습니다.")
        elif option == '2':
            while True:
                try:
                    new_price = int(input("새로운 가격 (정수로 입력): "))
                    self.products[product_name] = (new_price, self.products[product_name][1])  # 가격만 변경
                    print(f"'{product_name}'의 가격이 '{new_price}'으로 변경되었습니다.")
                    break
                except ValueError:
                    print("가격은 정수만 입력 가능합니다. 다시 시도해주세요.")

    # 상품 수정
    def update_product(self, product_name):
        if product_name not in self.products:
            print(f"'{product_name}' 상품이 존재하지 않습니다.")
            return
        print(f"수정할 항목 선택: \n1. 상품명\n2. 가격\n3. 수량")
        option = input("선택: ")
        if option == '1':
            new_name = input("새로운 상품명: ")
            self.products[new_name] = self.products.pop(product_name)
            print(f"'{product_name}'의 이름이 '{new_name}'으로 변경되었습니다.")
        elif option == '2':
            while True:
                try:
                    new_price = int(input("새로운 가격 (정수로 입력): "))
                    self.products[product_name] = (new_price, self.products[product_name][1])  # 가격만 변경
                    print(f"'{product_name}'의 가격이 '{new_price}'으로 변경되었습니다.")
                    break
                except ValueError:
                    print("가격은 정수만 입력 가능합니다. 다시 시도해주세요.")
        elif option == '3':
            while True:
                try:
                    new_quantity = int(input("새로운 수량 (정수로 입력): "))
                    self.products[product_name] = (self.products[product_name][0], new_quantity)  # 수량만 변경
                    print(f"'{product_name}'의 수량이 '{new_quantity}'으로 변경되었습니다.")
                    break
                except ValueError:
                    print("수량은 정수만 입력 가능합니다. 다시 시도해주세요.")
        else:
            print("잘못된 입력입니다.")

    # 상품 삭제 (단종)
    def remove_product(self):
        product_name = input("단종할 상품명: ")
        if product_name in self.products:
            del self.products[product_name]
            print(f"상품 '{product_name}'이(가) 삭제되었습니다.")
            self.save_items()
        else:
            print("해당 상품이 존재하지 않습니다.")

    # 상품 목록 조회
    def view_products(self):
        if not self.products:
            print("등록된 상품이 없습니다.")
        else:
            for product, (price, quantity) in self.products.items():
                print(f"{product}: {price}원, 수량: {quantity}")

    # 관리자용 상품 관리
    def manage_products(self):
        while True:
            print("\n1. 상품 조회\n2. 상품 등록\n3. 상품 수정\n4. 단종 등록\n0. 종료")
            choice = input("선택: ")
            if choice == '1':
                self.view_products()  # 상품 조회
            elif choice == '2':
                self.add_product()  # 상품 추가
            elif choice == '3':
                product_name = input("수정할 상품명을 입력하세요: ")
                self.update_product(product_name)  # 상품 수정
            elif choice == '4':
                self.remove_product()  # 상품 삭제
            elif choice == '0':
                print("상품 관리 화면을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다. 다시 선택하세요.")

    # 주문 추가 (고객용)
    # 주문 추가 (고객용)
    def add_order(self):
        customer_name = input("고객 이름: ")
        customer_address = input("고객 주소: ")
        
        while True:  # 상품 선택을 위한 루프 추가
            print("상품 목록:")
            self.view_products()
            
            product_name = input("주문할 상품명을 입력하세요 (0을 입력하면 종료): ")
            if product_name == '0':
                print("주문을 종료합니다.")
                return  # 주문 종료

            if product_name in self.products:
                product_price, product_quantity = self.products[product_name]
                
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
                            continue  # 수량이 초과할 경우 다시 입력 받음
                        break  # 유효한 수량이면 루프 종료
                    except ValueError:
                        print("수량은 정수로 입력해야 합니다.")
                        continue  # 유효하지 않은 수량이면 다시 입력 받음

                # 주문 날짜 입력
                while True:
                    input_date = input("주문 날짜를 입력하세요 (YYYY-MM-DD 또는 0을 입력하면 종료): ")
                    if input_date == '0':
                        print("주문을 종료합니다.")
                        return  # 주문 종료
                    
                    try:
                        year, month, day = map(int, input_date.split('-'))
                        order_date = datetime.date(year, month, day)
                        break
                    except ValueError:
                        print("잘못된 형식입니다. 다시 입력하세요.")
                
                order_id = f"ORD{random.randint(1000, 9999)}"
                order = Order(order_id, product_name, product_price, quantity, customer_name, customer_address, order_date)
                self.orders.append(order)

                # Update product quantity
                self.products[product_name] = (product_price, product_quantity - quantity)
                print(f"주문이 추가되었습니다: \n{order}")
                self.save_orders()
                self.save_sales(order)  # Save sales information
                break  # 주문이 성공적으로 추가되면 루프 종료
            else:
                print("해당 상품이 존재하지 않습니다. 다시 입력하세요.")


    # 매출 정보 저장
    def save_sales(self, order):
        with open('sales.txt', 'a', encoding='utf-8') as f:
            total_price = order.product_price * order.quantity
            f.write(f"{order.product_name},{order.quantity},{total_price}원,{order.order_date}\n")

    # 주문 삭제 (관리자용)
    def remove_order(self):
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
            for order in self.orders:
                print(order)

    # 매출 조회
    def view_sales(self):
        total_sales = 0
        print("\n매출 내역:")
        print(f"{'상품명':<10} {'수량':<10} {'총 가격':<10}")
        for order in self.orders:
            total_price = order.product_price * order.quantity
            print(f"{order.product_name:<10} {order.quantity:<10} {total_price:<10}원")
            total_sales += total_price
        print(f"총 매출액: {total_sales}원")

    # 파일로부터 상품 읽어오기
    def load_items(self):
        try:
            with open('products.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():  # Check if the line is not empty
                        product_name, product_price, product_quantity = line.strip().split(',')
                        self.products[product_name] = (int(product_price), int(product_quantity))  # 가격과 수량
        except FileNotFoundError:
            pass  # File not found, do nothing
        except ValueError:
            print("파일 형식이 잘못되었습니다. 상품 정보를 확인하세요.")  # Handle incorrect format

    # 상품을 파일에 저장
    def save_items(self):
        with open('products.txt', 'w', encoding='utf-8') as f:
            for product_name, (price, quantity) in self.products.items():
                f.write(f"{product_name},{price},{quantity}\n")

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
            print("\n1. 상품 목록 조회\n2. 주문하기\n0. 종료")
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
            print("\n1. 상품 목록 조회\n2. 주문 조회\n3. 주문 삭제\n4. 매출 조회\n0. 종료")
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
            print("\n1. 고객\n2. 관리자\n0. 종료")
            role = input("선택: ")
            if role == '1':
                self.customer_menu()  # 고객 메뉴로 이동
            elif role == '2':
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
