from django.core import paginator
from django.http import request
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import F, Sum, Count, Q
# from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from selenium import webdriver
from fake_useragent import UserAgent
# import re
import csv
from app01 import models


# Create your views here.

def add_book(request):
    if request.method == 'POST':
        # 從add_book.html所獲取的數據
        isbn = request.POST.get('isbn')
        bookname = request.POST.get('bookname')
        book_author = request.POST.get('book_author')
        book_publisher = request.POST.get('book_publisher')
        book_count = request.POST.get('book_count')
        # 輸入的ISBN與MYSQL當中的資料做比較，如果MYSQL當中已經有資料，則book_count增加
        if models.BookInfo.objects.filter(isbn=isbn):
            models.BookInfo.objects.filter(isbn=isbn).update(book_count=F("book_count")+book_count)
            return redirect('/app01/book_list/')

        # 輸入的ISBN與MYSQL當中的資料做比較，如果MYSQL當中沒有資料，則新增全新的資料
        else:
        # 保存到數據庫app01_book
            models.BookInfo.objects.create(isbn=isbn, bookname=bookname, book_author=book_author, book_publisher=book_publisher, book_count=book_count)
        # 重定向到圖書列表頁面
            return redirect('/app01/book_list/')
    return render(request, 'add_book.html')

def book_list(request):
    book_list = models.BookInfo.objects.all()
    print(book_list)
    paginator = Paginator(book_list, 15) # 每15個進行分頁
    page_num = request.GET.get('page', 1) # 獲取url的頁面參數(GET請求)
    page_of_book_list = paginator.get_page(page_num)
    currentr_page_num = page_of_book_list.number # 獲取當前頁碼
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1)) # 獲取當前頁碼前後各2頁的頁碼範圍
    # 加上省略頁碼標記
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append( '...')
    # 加上首頁和尾頁
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    
    
    # print(paginator.count)
    # print(paginator.num_pages)
    # print(paginator.page_range)
    # print(paginator.object_list)
    # print(paginator.page(2).start_index())
    
    context = {}
    context['book_list'] = page_of_book_list.object_list
    context['page_of_book_list'] = page_of_book_list
    context['page_range'] = page_range
    context['book_list_types'] = models.BookInfo.objects.all()
    return render(request, "book_list.html", context)

def edit_book(request):
    if request.method == "POST":
        # 1.獲取表單提交過來的內容
        id = request.POST.get('id')
        isbn = request.POST.get('isbn')
        bookname = request.POST.get('bookname')
        book_author = request.POST.get('book_author')
        book_publisher = request.POST.get('book_publisher')
        book_count = request.POST.get('book_count')
        # 2.根據id去數據庫查找對象
        book_obj = models.BookInfo.objects.get(id=id)
        # 3.修改
        book_obj.isbn = isbn
        book_obj.bookname = bookname
        book_obj.book_author = book_author
        book_obj.book_publisher = book_publisher
        book_obj.book_count = book_count
        book_obj.save()
        # 4.重定向到書本列表
        return redirect('/app01/book_list/')
    else:
        # 1.獲取id
        id = request.GET.get('id')
        # 2.去數據庫中查找相應的數據
        book_obj = models.BookInfo.objects.get(id=id)
        book_obj_list = models.BookInfo.objects.all()
        # 3.返回頁面
        return render(request, 'edit_book.html', {"book_obj":book_obj, "book_obj_list":book_obj_list})

def delete_book(request):
    # 1.獲取刪除圖書的id
    id = request.GET.get("id")
    # 2.根據id刪除數據庫中紀錄
    models.BookInfo.objects.filter(id=id).delete()
    return redirect("/app01/book_list/")

def author_list(request):
    # 依據數據庫的作者，查出該作者有多少本書
    author_count_list = models.BookInfo.objects.values("book_author").annotate(res_author_book_sum=Sum('book_count'), res_author_book_count=Count('bookname'))
    print(author_count_list)
    paginator = Paginator(author_count_list, 15) # 每15個進行分頁
    page_num = request.GET.get('page', 1) # 獲取url的頁面參數(GET請求)
    page_of_author_count_list = paginator.get_page(page_num)
    currentr_page_num = page_of_author_count_list.number # 獲取當前頁碼
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1)) # 獲取當前頁碼前後各2頁的頁碼範圍
    # 加上省略頁碼標記
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append( '...')
    # 加上首頁和尾頁
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context = {}
    context['author_count_list'] = page_of_author_count_list.object_list
    context['page_of_author_count_list'] = page_of_author_count_list
    context['page_range'] = page_range
    context['author_count_list_types'] = models.BookInfo.objects.values("book_author").annotate(res_author_book_sum=Sum('book_count'), res_author_book_count=Count('bookname'))
    print(context)
    return render(request, "author_list.html", context)

def edit_author(request):
    if request.method == 'POST':
        book_author = request.POST.get('book_author')
        book_author_get = request.GET.get('book_author')
        print(book_author)
        print(book_author_get)
        book_author_obj_list = models.BookInfo.objects.filter(book_author=book_author_get)
        print(book_author_obj_list)
        # # book_author_obj.book_author = book_author
        book_author_obj_list.update(book_author=book_author)
        return redirect('/app01/author_list/')
    else:
        book_author = request.GET.get('book_author')
        book_author_obj = models.BookInfo.objects.filter(book_author=book_author)[0]
        book_author_obj_list = models.BookInfo.objects.all()
        # 3.返回頁面
        return render(request, 'edit_author.html', {"book_author_obj":book_author_obj, "book_author_obj_list":book_author_obj_list})

def delete_author(request):
    book_author = request.GET.get("book_author")
    print(book_author)
    models.BookInfo.objects.filter(book_author=book_author).delete()
    return redirect("/app01/author_list/")

def publisher_list(request):
    # 依據數據庫的出版社，查出該出版社有多少本書
    publisher_count_list = models.BookInfo.objects.values("book_publisher").annotate(res_publisher_book_sum=Sum('book_count'), res_publisher_book_count=Count('bookname'))
    print(publisher_count_list)
    paginator = Paginator(publisher_count_list, 15) # 每15個進行分頁
    page_num = request.GET.get('page', 1) # 獲取url的頁面參數(GET請求)
    page_of_publisher_count_list = paginator.get_page(page_num)
    currentr_page_num = page_of_publisher_count_list.number # 獲取當前頁碼
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1)) # 獲取當前頁碼前後各2頁的頁碼範圍
    # 加上省略頁碼標記
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append( '...')
    # 加上首頁和尾頁
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context = {}
    context['publisher_count_list'] = page_of_publisher_count_list.object_list
    context['page_of_publisher_count_list'] = page_of_publisher_count_list
    context['page_range'] = page_range
    context['publisher_count_list_types'] = models.BookInfo.objects.values("book_publisher").annotate(res_publisher_book_sum=Sum('book_count'), res_publisher_book_count=Count('bookname'))
    print(context)
    return render(request, "publisher_list.html", context)

def edit_publisher(request):
    if request.method == 'POST':
        book_publisher = request.POST.get('book_publisher')
        book_publisher_get = request.GET.get('book_publisher')
        print(book_publisher)
        print(book_publisher_get)
        book_publisher_obj_list = models.BookInfo.objects.filter(book_publisher=book_publisher_get)
        print(book_publisher_obj_list)
        # # book_publisher_obj.book_publisher = book_publisher
        book_publisher_obj_list.update(book_publisher=book_publisher)
        return redirect('/app01/publisher_list/')
    else:
        book_publisher = request.GET.get('book_publisher')
        book_publisher_obj = models.BookInfo.objects.filter(book_publisher=book_publisher)[0]
        book_publisher_obj_list = models.BookInfo.objects.all()
        # 3.返回頁面
        return render(request, 'edit_publisher.html', {"book_publisher_obj":book_publisher_obj, "book_publisher_obj_list":book_publisher_obj_list})

def delete_publisher(request):
    book_publisher = request.GET.get("book_publisher")
    print(book_publisher)
    models.BookInfo.objects.filter(book_publisher=book_publisher).delete()
    return redirect("/app01/publisher_list/")

def add_book_isbn(request):
    if request.method == 'POST':
        # 從add_book_isbn.html所獲取的數據
        isbn = request.POST.get('isbn')
        # 輸入的ISBN與MYSQL當中的資料做比較，如果MYSQL當中已經有資料，則book_count+1
        if models.BookInfo.objects.filter(isbn=isbn):
            models.BookInfo.objects.filter(isbn=isbn).update(book_count=F("book_count")+1)
            return redirect('/app01/book_list/')
        # 輸入的ISBN與MYSQL當中的資料做比較，如果MYSQL當中沒有資料，則新增全新的資料
        else:
            # 無頭瀏覽器的設置
            options = webdriver.FirefoxOptions()
            # 不開啟實體瀏覽器直接執行
            options.add_argument('--headless')
            # 開啟無痕模式
            options.add_argument("--incognito")
            # 讓 selenium透過 tor訪問 internet
            proxy = "socks5://localhost:9050"
            options.add_argument('--proxy-server={}'.format(proxy))  
            # 使用偽造的user-agent
            options.add_argument("user-agent={}".format(UserAgent().random)) 
            # 1.打開Firefox瀏覽器
            driver = webdriver.Firefox(options=options)
            # 2.在瀏覽器地址欄輸入URL地址，並確認
            driver.get('http://isbn.ncl.edu.tw/NEW_ISBNNet/H30_SearchBooks.php?&Pact=DisplayAll4Simple')
            # 3.找到搜索框節點，並發送文本-
            driver.find_element_by_xpath('//*[@id="FO_SearchValue0"]').send_keys(isbn)
            # 4.找到搜索按鈕，並進行模擬點擊
            driver.find_element_by_xpath('/html/body/section/div/div/div[2]/div[2]/form[1]/div[2]/a').click()
            driver.find_element_by_xpath('/html/body/section/div/div/div[2]/div[2]/form[1]/div[2]/a').click()
            # 5.找到節點
            # 書本名稱
            bookname = driver.find_element_by_xpath('/html/body/section/div/div/div[2]/div[2]/form[1]/div[6]/table/tbody/tr[2]/td[3]/a').text
            # 書本作者
            # 把作者欄位當中"; "replace成"。 "避免轉換成CSV時造成錯誤
            book_author = driver.find_element_by_xpath('/html/body/section/div/div/div[2]/div[2]/form[1]/div[6]/table/tbody/tr[2]/td[4]').text.replace('; ', '。 ')        
            # 書本出版社
            book_publisher = driver.find_element_by_xpath('/html/body/section/div/div/div[2]/div[2]/form[1]/div[6]/table/tbody/tr[2]/td[5]/font').text
            # 保存到數據庫app01_book
            models.BookInfo.objects.create(isbn=isbn, bookname=bookname, book_author=book_author, book_publisher=book_publisher, book_count=1)
            # 關閉瀏覽器
            driver.quit()
            # 重定向到圖書列表頁面
            return redirect('/app01/book_list/')
    return render(request, 'add_book_isbn.html')

def make_csv_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="booklist.csv"'
    book_list = models.BookInfo.objects.all()
    writer = csv.writer(response)
    writer.writerow(['id', 'isbn', 'bookname', 'book_author', 'book_publisher', 'book_count'])
    for b in book_list:
        writer.writerow([b.id, b.isbn, b.bookname, b.book_author, b.book_publisher, b.book_count])
    return response


# def book_search_list(request):
#     if request.method == "POST":
#         book_list_search = request.POST.get('book_list_search')
#         print(book_list_search)
#         search_1 = models.BookInfo.objects.filter(Q(book_name="book_list_search") | Q(book_author="book_list_search") | Q(book_publisher="book_list_search"))
#         print(search_1)


