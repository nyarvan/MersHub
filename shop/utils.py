import openpyxl
from slugify import slugify
import boto3
from MersHub.settings import MEDIA_URL, STATIC_ROOT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
from shop.models import Category, Product
import os.path

category_dict = {
    'Капоты': 'Капот',
    'Петли капота': 'Капот',
    'Крылья': 'Крила',
    'Рейлинги': 'Кузов',
    'пластик': 'Кузов',
    'Подкрылки': 'Крила',
    'Ручки': 'Ручки',
    'Кронштейны ручек': 'Ручки',
    'Стекла': 'Стекла',
    'Резинки': 'Стекла',
    'Двери': 'Двері',
    '}{ром дверей': 'Двері',
    'Двери 1эт': 'Двері',
    'Двери  2эт.': 'Двері',
    'Багажнки': 'Багажник',
    'Бампера': 'Бампера',
    'Усилители бамперов': 'Бампера',
    'Пороги': 'Пороги',
    'Блоки розжига': 'Блоки',
    'Фары': 'Фари',
    'Фонари': 'Ліхтарі',
    'Проводка бампеов': 'Проводки',
    'Датчики': 'Датчики',
    'Лямбды': 'Датчики',
    'Радары': 'Датчики',
    'Кулаки': 'Кулаки',
    'Цапфы': 'Кулаки',
    'Рычаги': 'Важелі',
    'Педали': 'Педалі',
    'Подрамники': 'Підрамники',
    'Полуоси промвалы': 'Пів осі',
    'Карданы': 'Кардани',
    'АКПП': 'Коробки передач',
    'Аморты': 'Амортизатор',
    'Аморты капота': 'Амортизатор',
    'Суппорты': 'Супорти',
    'Редуктора': 'Редуктори',
    'Раздатки': 'Роздатки',
    'Моторы': 'Мотори',
    'Салоны': 'Салони',
    'Обшивка': 'Обшивка',
    'Рули': 'Кермо',
    'Рулевые колонки': 'Кермо',
    'Рейки': 'Кермо',
    'Безопасность': 'Безпека',
    'Подушки в руль': 'Безпека',
    'Защиты ДВС': 'Безпека',
    'Защиты днища': 'Безпека',
    'Замки разные': 'Замки',
    'Замки дверей': 'Замки',
    'Решетки': 'Інсталяційна панель (телевізори)',
    'Радиаторы': 'Вентилятор радіаторів'
}


def download_excel(filename):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3.download_file(AWS_STORAGE_BUCKET_NAME, f'files/{filename}', f'{STATIC_ROOT}\\files\\{filename}')


def excel_products(filename, min_col=2, max_col=6, min_row=2):
    if not os.path.exists('{STATIC_ROOT}\\files\\{filename}'):
        download_excel(filename)
    wb = openpyxl.load_workbook(f'{STATIC_ROOT}\\files\\{filename}')
    ws = wb.active
    products_cnt = 0

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
            
            if isinstance(id, str) and isinstance(price, (int, float)) and isinstance(count, int) and isinstance(used_quantity, int):
                if id and count and len(id) == 11 and count > 0:
                    product = Product.objects.filter(id=row[0]).exists()
                    if not product:
                        Product.objects.create(category=category.first(), id=id, slug=slugify(f'{id}-{name}'), name=name, price=price, count=count, used_quantity=used_quantity)
                        products_cnt += 1

    return f'{products_cnt} products have been added to the site'
