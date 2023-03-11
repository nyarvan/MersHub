import openpyxl
from slugify import slugify
from MersHub.settings import MEDIA_URL
from shop.models import Category, Product

category_dict = {
    'Капоты': 'Капот',
    'Крылья': 'Крила',
    'Двери': 'Двері',
    'Бампера': 'Бампера',
    'Блоки розжига': 'Блоки',
    'Фары': 'Фари',
    'Фонари': 'Ліхтарі',
    'Проводка': 'Проводки',
    'Датчики': 'Датчики',
    'Кулаки': 'Кулаки',
    'Рычаги': 'Важелі',
    'Подрамники': 'Підрамники',
    'Полуоси': 'Пів осі',
    'Карданы': 'Кардани',
    'АКПП': 'Коробки передач',
    'Редукторы': 'Редуктори',
    'Раздатки': 'Роздатки',
    'Моторы': 'Мотори',
    'Салоны': 'Салони',
    'Радиаторы': 'Вентилятор радіаторів'
}

def excel_products(filename, min_col, max_col, min_row):
    wb = openpyxl.load_workbook(f'{MEDIA_URL}//images//files//{filename}')
    ws = wb.active

    for page in wb.sheetnames:
        if page not in category_dict.keys():
            continue
        ws = wb[page]
        category = Category.objects.filter(name=category_dict[page])
        if not category.exists():
            continue
        for row in ws.iter_rows(min_col=min_col, max_col=max_col, min_row=min_row, values_only=True):
            id = row[0]
            name = row[1]
            price = row[2]
            count = row[3]
            used_quantity = row[4]
            
            if isinstance(id, str) and isinstance(name, str) and isinstance(price, (int, float)) and isinstance(count, int) and isinstance(used_quantity, int):
                if id and name and price and count and len(id) == 11  and price > 0  and count > 0:
                    product = Product.objects.filter(id=row[0]).exists()
                    if not product:
                        Product.objects.create(category=category.first(), id=id, slug=slugify(f'{id}-{name}'), name=name, price=price, count=count, used_quantity=used_quantity)
