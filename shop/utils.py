import openpyxl
from slugify import slugify
import boto3
from MersHub.settings import MEDIA_URL, STATIC_ROOT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
from shop.models import Category, Product
import os.path

category_dict = {
    'Капоты': 'Капот',
    'Крылья': 'Крила',
    'Подкрылки': 'Крила',
    'Двери': 'Двері',
    'Бампера': 'Бампера',
    'Блоки розжига': 'Блоки',
    'Фары': 'Фари',
    'Фонари': 'Ліхтарі',
    'Проводка бампеов': 'Проводки',
    'Датчики': 'Датчики',
    'Радары': 'Датчики',
    'Кулаки': 'Кулаки',
    'Рычаги': 'Важелі',
    'Подрамники': 'Підрамники',
    'Полуоси': 'Пів осі',
    'Карданы': 'Кардани',
    'АКПП': 'Коробки передач',
    'Редукторы': 'Редуктори',
    'Раздатки': 'Роздатки',
    'Моторы': 'Мотори',
    'АКПП': 'Мотори',
    'Салоны': 'Салони',
    'Радиаторы': 'Інсталяційна панель (телевізори)',
    'Вентилятор': 'Вентилятор радіаторів'
}


def download_excel(filename):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3.download_file(AWS_STORAGE_BUCKET_NAME, f'files/{filename}', f'{STATIC_ROOT}\\files\\{filename}')


def excel_products(filename, min_col=2, max_col=6, min_row=2):
    if not os.path.exists('{STATIC_ROOT}\\files\\{filename}'):
        download_excel(filename)
    wb = openpyxl.load_workbook(f'{STATIC_ROOT}\\files\\{filename}')
    ws = wb.active
    count = 0

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
                        count += 1

    return f'{count} products have been added to the site'
