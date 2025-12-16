class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.is_available = True
        self.borrower_id = None
    
    def borrow(self, user_id):
        if self.is_available:
            self.is_available = False
            self.borrower_id = user_id
            return True
        return False
    
    def return_book(self):
        if not self.is_available:
            self.is_available = True
            self.borrower_id = None
            return True
        return False
    
    def is_book_available(self):
        return self.is_available
    
    def get_status(self):
        return "可借阅" if self.is_available else f"已借出({self.borrower_id})"

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []
    
    def can_borrow_more(self):
        return len(self.borrowed_books) < 3
    
    def borrow_book(self, book):
        if self.can_borrow_more():
            self.borrowed_books.append(book)
            return True
        print(f"{self.name}已达到最大借阅数量")
        return False
    
    def return_book(self, book_isbn):
        for i, book in enumerate(self.borrowed_books):
            if book.isbn == book_isbn:
                return self.borrowed_books.pop(i)
        return None

class Library:
    def __init__(self):
        self.books = {}
        self.users = {}
    
    def add_book(self, book):
        if book.isbn not in self.books:
            self.books[book.isbn] = book
            print(f"添加书籍《{book.title}》")
            return True
        print(f"ISBN {book.isbn}已存在")
        return False
    
    def add_user(self, user):
        if user.user_id not in self.users:
            self.users[user.user_id] = user
            print(f"添加用户{user.name}")
            return True
        print(f"用户ID {user.user_id}已存在")
        return False
    
    def borrow_book(self, user_id, isbn):
        if user_id not in self.users:
            print(f"用户ID {user_id}不存在")
            return False
        
        if isbn not in self.books:
            print(f"ISBN {isbn}不存在")
            return False
        
        user = self.users[user_id]
        book = self.books[isbn]
        
        if not user.can_borrow_more():
            print(f"{user.name}已达到最大借阅数量")
            return False
        
        if not book.is_book_available():
            print(f"《{book.title}》已被借出")
            return False
        
        if book.borrow(user_id) and user.borrow_book(book):
            print(f"{user.name}借阅《{book.title}》成功")
            return True
        return False
    
    def return_book(self, user_id, isbn):
        if user_id not in self.users:
            print(f"用户ID {user_id}不存在")
            return False
        
        if isbn not in self.books:
            print(f"ISBN {isbn}不存在")
            return False
        
        user = self.users[user_id]
        book = self.books[isbn]
        
        if book.borrower_id != user_id:
            print(f"《{book.title}》不是{user.name}借阅的")
            return False
        
        returned_book = user.return_book(isbn)
        if returned_book and book.return_book():
            print(f"{user.name}归还《{book.title}》成功")
            return True
        return False
    
    def check_book_availability(self, isbn):
        if isbn in self.books:
            book = self.books[isbn]
            return book.is_book_available()
        print(f"ISBN {isbn}不存在")
        return False
    
    def list_books(self):
        print("图书馆藏书:")
        if not self.books:
            print("  暂无藏书")
        else:
            for book in self.books.values():
                print(f"  《{book.title}》- {book.author} - {book.get_status()}")
    
    def list_users(self):
        print("注册用户:")
        if not self.users:
            print("  暂无用户")
        else:
            for user in self.users.values():
                print(f"  {user.name}(ID:{user.user_id})-借阅{len(user.borrowed_books)}本")

if __name__ == "__main__":
    library = Library()
    
    book1 = Book("001", "Python编程", "张三")
    book2 = Book("002", "算法导论", "李四")
    
    library.add_book(book1)
    library.add_book(book2)
    
    user1 = User("U01", "王五")
    user2 = User("U02", "赵六")
    
    library.add_user(user1)
    library.add_user(user2)
    
    print("\n初始状态:")
    library.list_books()
    library.list_users()
    
    print("\n借书测试:")
    library.borrow_book("U01", "001")
    library.borrow_book("U01", "002")
    library.borrow_book("U02", "001")
    
    print("\n检查书籍状态:")
    available = library.check_book_availability("001")
    print(f"书籍001可借: {'是' if available else '否'}")
    
    print("\n当前状态:")
    library.list_books()
    
    print("\n还书测试:")
    library.return_book("U01", "001")
    
    print("\n最终状态:")
    library.list_books()
    library.list_users()
