from django.db import models

# Create your models here.
# https://isbn.ncl.edu.tw/NEW_ISBNNet/H30_SearchBooks.php?&Pact=DisplayAll4Simple  的欄位有：書名 	作者 	出版者 	日期 	適讀對象 	分級註記
class BookInfo(models.Model):
    # 1.ID
    id = models.AutoField(primary_key=True)
    # 2.ISBN
    isbn = models.BigIntegerField(null=False)
    # 3.書名
    bookname = models.TextField(null=False)
    # 4.書本的作者
    book_author = models.TextField(null=False)
    # 5.書本的出版社
    book_publisher = models.TextField(null=False)
    # 6.書本的數量
    book_count = models.IntegerField(null=False)

    def __str__(self):
        return '%s_%s_%s_%s_%s_%s'%(self.id, self.isbn, self.bookname, self.book_author, self.book_publisher, self.book_count)
    # 會造成annotate的錯誤，因此注䆁掉
    # class Meta:
        # ordering = ['id']
        