import pymysql


class Database:
    """Клас для взаємодії з базою даних"""

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', passwd='', db='site_bd')
        self.cursor = self.conn.cursor()

    def select_event_on_this_week(self):
        """Метод, який виводить усі події на тиждень"""

        res = ""
        self.cursor.execute("""SELECT title, name, text, DATE_FORMAT(create_date, '%d.%m.%y') 
        FROM news INNER JOIN category ON news.category_id=category.id 
        WHERE YEAR(`create_date`) = YEAR(NOW()) AND WEEK(`create_date`, 1) = WEEK(NOW(), 1)
        ORDER BY create_date;""")
        for row in self.cursor:
            res += "Назва: " + row[0] + "\n" + "Категорія: " + row[1] + "\n" + "Текст: " + row[
                2] + "\n" + "Дата: " + str(row[3]) + "\n" + "\n" \
                   + "====================" + "\n" + "\n"
        return res

    def select_event_today(self):
        """Метод, який виводить усі події на сьогодні"""

        res = ""
        self.cursor.execute("""SELECT title, name, text, DATE_FORMAT(create_date, '%d.%m.%y') 
        FROM news INNER JOIN category ON news.category_id=category.id 
        WHERE DAY(`create_date`) = DAY(NOW()) AND MONTH(`create_date`) = MONTH(NOW()) AND YEAR(`create_date`) = YEAR(NOW())
        ORDER BY create_date;""")
        for row in self.cursor:
            res += "Назва: " + row[0] + "\n" + "Категорія: " + row[1] + "\n" + "Текст: " + row[
                2] + "\n" + "Дата:" + str(row[3]) + "\n" + "\n" \
                   + "====================" + "\n" + "\n"
        return res

    def select_event_on_this_month(self):
        """Метод, який виводить усі події на поточний місяць"""

        res = ""
        self.cursor.execute("""SELECT title, name, text, DATE_FORMAT(create_date, '%d.%m.%y') 
        FROM news INNER JOIN category ON news.category_id=category.id
        WHERE MONTH(`create_date`) = MONTH(NOW()) AND YEAR(`create_date`) = YEAR(NOW())
        ORDER BY create_date;""")
        for row in self.cursor:
            res += "Назва: " + row[0] + "\n" + "Категорія: " + row[1] + "\n" + "Текст: " + row[2] + "\n" + "Дата:"\
                   + str(row[3]) + "\n" + "\n" \
                   + "====================" + "\n" + "\n"
        return res

    def select_event_where_name(self, input):
        """Метод виводить події по заданій назві"""

        res = ""
        self.cursor.execute("""SELECT title, name, text, DATE_FORMAT(create_date, '%d.%m.%y') 
                FROM news INNER JOIN category ON news.category_id=category.id
                WHERE title like '%{0}%'
                ORDER BY create_date;""".format(input))
        for row in self.cursor:
            res += "Назва: " + row[0] + "\n" + "Категорія: " + row[1] + "\n" + "Текст: " + row[
                2] + "\n" + "Дата:" \
                   + str(row[3]) + "\n" + "\n" \
                   + "====================" + "\n" + "\n"
        return res

    def select_event_where_date(self, input): #  update._effective_user.id
        """Метод виводить події по вказаній даті"""

        res = ""
        self.cursor.execute("""SELECT title, name, text, DATE_FORMAT(create_date, '%d.%m.%y') 
                        FROM news INNER JOIN category ON news.category_id=category.id
                        WHERE DATE_FORMAT(create_date, '%d.%m.%y') like '%{0}%'
                        ORDER BY create_date;""".format(input))
        for row in self.cursor:
            res += "Назва: " + row[0] + "\n" + "Категорія: " + row[1] + "\n" + "Текст: " + row[
                2] + "\n" + "Дата:" \
                   + str(row[3]) + "\n" + "\n" \
                   + "====================" + "\n" + "\n"
        return res


if __name__ == '__main__':
    db = Database()
