# -*- coding: utf-8 -*-
import os, shutil
OUT="dist"  # the folder that gets published; nothing else from the project goes online

import re as _re
from i18n import EN
_KEYS=sorted(EN,key=len,reverse=True)
def translate(html):
    for k in _KEYS: html=html.replace(k,EN[k])
    return html

SITE=""     # после покупки домена впишите сюда адрес, например "https://emblem-a.ru", и запустите: python3 build.py
METRIKA=""  # номер счётчика Яндекс Метрики (только цифры), если подключите
# GitHub Pages builds pass the address in SITE_URL; a local build keeps SITE above
SITE=os.environ.get("SITE_URL",SITE).rstrip("/")
from urllib.parse import urlparse as _urlparse
BASE=(_urlparse(SITE).path.rstrip("/")+"/") if SITE else "/"   # "/" on your own domain, "/myportfolio/" on GitHub Pages

RATE=84.95  # RUB per USD, fallback (open.er-api.com, 7 Oct 2026); live rate is fetched in the browser
def usd_round(r):
    u=r/RATE
    s=5 if u<100 else 10
    return max(s,int(round(u/s))*s)
def usd(html):
    def f(m):
        rub=int(m.group(2).replace(",",""))
        return f'{m.group(1)}<span class="usd" data-rub="{rub}">${usd_round(rub):,}</span>'
    return _re.sub(r'(from )([\d,]+) ₽',f,html)

def langmenu(cur,ru_href,en_href,lab):
    def it(code,name,href):
        if code==cur: return f'<span class="lf on" aria-current="true" lang="{code}" title="{name}">{code.upper()}<i class="sr"> {name}</i></span>'
        return f'<a class="lf" href="{href}" hreflang="{code}" lang="{code}" data-lang="{code}" title="{name}">{code.upper()}<i class="sr"> {name}</i></a>'
    return f'<div class="langflags" role="group" aria-label="{lab}">'+it("ru","Русский",ru_href)+'<span class="lsep" aria-hidden="true">/</span>'+it("en","English",en_href)+'</div>'
shutil.rmtree(OUT,ignore_errors=True)
os.makedirs(OUT)
shutil.copytree("assets",os.path.join(OUT,"assets"),ignore=shutil.ignore_patterns(".DS_Store"))
# headers for hosts that read a _headers file (Netlify, Cloudflare Pages); other hosts: set the same headers in their panel
open(os.path.join(OUT,"_headers"),"w").write("""/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000
  Content-Security-Policy: frame-ancestors 'none'
""")

def W(name,html):
    ru=html.replace('<!--LANG-->',langmenu("ru",name,"en/"+name,"Язык"))
    ru=ru.replace('<!--USDNOTE-->','')
    ru=ru.replace('</head>',f'<link rel="alternate" hreflang="ru" href="{name}"><link rel="alternate" hreflang="en" href="en/{name}"></head>',1)
    if SITE: ru=ru.replace('</head>',f'<link rel="canonical" href="{SITE}/{name}"><meta property="og:url" content="{SITE}/{name}"></head>',1)
    open(os.path.join(OUT,name),"w",encoding="utf-8").write(ru)
    en=html.replace('<!--LANG-->',langmenu("en","../"+name,name,"Language"))
    en=en.replace('</head>',f'<link rel="alternate" hreflang="ru" href="../{name}"><link rel="alternate" hreflang="en" href="{name}"></head>',1)
    en=usd(translate(en).replace('<!--USDNOTE-->','<p class="usdnote">Dollar amounts are approximate: they are converted from rubles at the current exchange rate.</p>')).replace('<html lang="ru">','<html lang="en">')
    en=_re.sub(r'(href|src|poster)="assets/',r'\1="../assets/',en)
    os.makedirs(os.path.join(OUT,"en"),exist_ok=True)
    en=en.replace('og:locale" content="ru_RU"','og:locale" content="en_US"')
    if SITE: en=en.replace('</head>',f'<link rel="canonical" href="{SITE}/en/{name}"><meta property="og:url" content="{SITE}/en/{name}"></head>',1)
    open(os.path.join(OUT,"en",name),"w",encoding="utf-8").write(en)

D="https://drive.google.com/drive/folders/"
ROOT=D+"1vyIKsEkBskZMSDfxXAKTZHvZqFlVz9D2"
I={
 "tg":'<path d="M21 4 3 11l6 2 2 6 3-4 5 3z"/><path d="m9 13 12-9"/>',
 "mail":'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 "phone":'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 "arrow":'<path d="M5 12h14M13 6l6 6-6 6"/>',
 "ext":'<path d="M7 17 17 7M8 7h9v9"/>',
 "play":'<path d="M8 5v14l11-7z" fill="currentColor"/>',
 "film":'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 9h4M17 9h4M3 15h4M17 15h4"/>',
 "spark":'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z"/>',
 "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "wallet":'<path d="M3 7a2 2 0 0 1 2-2h13v4"/><path d="M3 7v11a2 2 0 0 0 2 2h15V9H5a2 2 0 0 1-2-2z"/><circle cx="16.5" cy="14.5" r="1"/>',
 "layers":'<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
 "wand":'<path d="m4 20 11-11"/><path d="m14 4 1 2 2 1-2 1-1 2-1-2-2-1 2-1zM19 12l.7 1.3L21 14l-1.3.7L19 16l-.7-1.3L17 14l1.3-.7z"/>',
 "target":'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
 "globe":'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
 "menu":'<path d="M4 7h16M4 12h16M4 17h16"/>',
 "check":'<path d="m5 12 5 5 9-10"/>',
 "chev":'<path d="m6 9 6 6 6-6"/>',
 "chart":'<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
}
def ico(n,c="ico"): return f'<svg class="{c}" viewBox="0 0 24 24" aria-hidden="true">{I[n]}</svg>'

# slug,title,cat,short,gradient,tab,driveid,internal
C=[
 ("yoshida","Yoshida & Co","Fashion","Творческий видеоролик для японского бренда сумок","g-b","#E0C4D4","1E9QL7Lwm4-QlSr-BMKJGShXsN3NpHXMA",1),
 ("magnit","Магнит — лучший наставник","Корпоративное событие","Ролик для ежегодной церемонии награждения «Лучший наставник»","g-a","#E0C4D4","1YrxKGVtPHGn40Dom2YiFPATafr99z3aX",1),
 ("vladkon","Владкон — конфеты на цветущем дереве","Имиджевый ролик","Ролик о производителе сладостей из Беларуси после ребрендинга","g-d","#D7B3C7","1lYZeneFuRNMBW6K4De6c3y--5dj-0nZ7",1),
 ("kubok-sbera","Кубок Сбера по хоккею","Спорт · ивент","Видео для открытия матча, отсчёт и ролики для баннеров на арене","g-e","#C9A0B9","1t2r2gVXo2wFXyqkyTFA3uQ1e790UBife",1),
 ("khl-monopoly","КХЛ Монополия","Реклама","15-секундный рекламный ролик для новой игры «Монополия» совместно с КХЛ","g-c","#E6D0DC","18aQcKZTrhkQeTK9lnKocTPzeaULb5wgU",1),
 ("cakes","Реклама упаковки для десертов","Фестиваль","Превью-ролик о кондитерской упаковке для фестиваля","g-f","#D7B3C7","1WYQBu8epQX9_sgtHCnMNI4eYRPC4ESJM",1),
 ("zargus","Zargus","Ритейл","Превью-ролик для нового салона мужской одежды","g-a","#D7B3C7","1DT4rBBoE5UuhW8edhvQb9nWiJ8wVXwCW",1),
]
VID={"zargus":"1L8DwJ8DTzzenAmrO4e8h3UqjFNEQhvr-","kubok-sbera":"1hKxhLr7sQnLaHl3ttOsvkGG50tOlelVf","khl-monopoly":"1reeV7LDRIrSlmqmuLUbheuQUIDZoeXga","yoshida":"1iIciyuS_uXgb5VB4Phpab9sn0KvyLrV0","magnit":"1CZL3ovk1BQ6IkZj-T68QAHtaYdZXP1Hs","cakes":"1R0eAyxjMyr69pFWxhhC12rimYX5I0Uya","vladkon":"1ZqfMx8ZTW4qp8HCZxRNhRqaTeYihlka0"}
CASES={
"magnit":dict(blocks=[("Задача","Компания готовила внутреннее мероприятие: ежегодное награждение лучших наставников. По техзаданию нужно было показать мастера и подмастерья, которые передают знания и вместе создают скульптуру."),("Идея","Сначала я написала сценарий в нескольких вариантах. Остановились на идее времени: Магнит — компания с большой историей, и ролик показывает, как опыт передаётся из поколения в поколение."),("Срок","14 дней."),("Результат","Превью-ролик открыл внутреннее мероприятие компании — церемонию «Лучший наставник».")],
 steps=[("Герои","Продумала внешность и одежду героев каждой эпохи: наставник и ученик меняются вместе со временем, и по одежде и инструментам читается смена поколений."),("Мастерская","Подобрала место действия: свет, инструменты, фактуры камня."),("Ключевые кадры","Отдельная картинка для каждой сцены: работа над глыбой, появление логотипа, надпись «Лучший наставник». Кадры согласовывались с заказчиком до начала видео."),("Видео","Оживила утверждённые кадры и сделала плавные переходы между эпохами."),("Финал","Последний кадр с логотипом в золотом свете.")],
 imgs=[("magnit-1","Эпоха 1 · Зарождение"),("magnit-2","Эпоха 2 · Возрождение"),("magnit-3","Эпоха 3 · Индустриализация"),("magnit-4","Эпоха 4 · Середина XX века"),("magnit-5","Эпоха 5 · 90-е"),("magnit-6","Эпоха 6 · Современность"),("magnit-7","Финал: логотип в золотом свечении")],
 epochs=[("Эпоха 1 · Зарождение","Оригинальный старт. Ракурс снизу вверх, тёмная мастерская. Наставник и его первый ученик работают над грубой мраморной глыбой в человеческий рост: наставник направляет руку ученика с резцом, летят искры, тёплый золотой свет."),("Эпоха 2 · Возрождение","Плавный переход: камера огибает камень. У глыбы уже наставник и новый ученик. Они высекают слева форму метки, как на карте, — часть логотипа Магнита, и камень начинает приобретать очертания."),("Эпоха 3 · Индустриализация","Снова переход. Мастера следующего поколения — в кепках и подтяжках — механическими инструментами вырезают внутри метки силуэт рукопожатия. В окнах мастерской появляются красные и синие световые блики."),("Эпоха 4 · Середина XX века","Камера берёт средний план. Женская пара скульпторов формирует верхнюю строку надписи «Лучший». Пыль мягко подсвечивается золотым лучом."),("Эпоха 5 · 90-е","Двое мужчин в рабочей одежде 90-х вместе работают над словом «Наставник»: надпись под их руками проступает всё чётче."),("Эпоха 6 · Современность","Финальный штрих. Современная пара мастеров ювелирно сдувает пыль с идеально ровной скульптуры, наставник одобряюще кивает. Скульптура начинает излучать мощное, торжественное золотое свечение.")]),
"vladkon":dict(blocks=[("Задача","Компания прошла ребрендинг: обновила позиционирование и всю дизайн-систему. Нужен был ролик о компании после изменений, который можно показывать партнёрам на переговорах как вступление и использовать внутри компании."),("Идея","Основа — новый логотип компании: цветы на дереве. Дерево вырастает и расцветает на рассвете, что символизирует начало новой истории и рост компании. Вместо плодов на ветках настоящие конфеты, которые компания производит и которые можно купить."),("Срок","8 дней."),("Результат","Внутренний корпоративный ролик для партнёров, который показывает компанию после ребрендинга.")],
 steps=[("Концепция","Разбор логотипа и поиск образа, который его продолжает."),("Ключевые кадры","Дерево, рассвет, поле. Сделала несколько вариантов композиции и цвета, включая вариант в фиолетовой гамме."),("Конфеты","Взяла настоящие упаковки продукции, чтобы на экране были именно те конфеты, которые увидит покупатель."),("Выбор варианта","Показала заказчику несколько вариантов кадра, вместе выбрали итоговый."),("Видео","Оживила кадры: дерево вырастает на рассвете.")],
 imgs=[("vladkon-1","Вариант композиции 1"),("vladkon-2","Вариант в фиолетовой гамме"),("vladkon-3","Вариант композиции 3"),("vladkon-4","Вариант композиции 4"),("vladkon-5","Итоговый кадр")],
 note="Показываю варианты до того, как начинаю делать видео"),
"cakes":dict(blocks=[("Задача","Заказчик производит упаковку для кондитерских изделий. Ролик нужен, чтобы показать продукцию на фестивале."),("Идея","По желанию заказчика ролик начинается с роскошной пекарни: красные витрины, посетители покупают торт в фирменной упаковке. Затем история идёт дальше: покупка, подарок, праздничный ужин. Упаковка проходит через весь сюжет. Вторая часть ролика — 3D-демонстрация упаковки."),("Срок","10–11 дней."),("Результат","Ролик для демонстрации упаковки на фестивале.")],
 steps=[("Сценарий","Раскадровка по сценам: пекарня, выход на улицу, встреча, ужин."),("Интерьер и герои","Создала пекарню в фирменных цветах и героев, узнаваемых в каждой сцене."),("Упаковка в кадре","Следила, чтобы форма, цвет и логотип упаковки были одинаковыми во всех сценах."),("3D-часть","3D-демонстрацию упаковки по просьбе заказчика делал другой подрядчик, я встроила её в общий ролик."),("Варианты упаковки","После 3D-части сгенерировала нейросетью кадры с разными вариациями упаковки, чтобы показать ассортимент."),("Сборка","Соединила все части в один ролик.")],
 imgs=[("cakes-1","Вход в пекарню"),("cakes-2","Покупка торта в фирменной упаковке"),("cakes-3","Подарок: выход на улицу"),("cakes-4","Праздничный ужин"),("cakes-5","Упаковка в кадре"),("cakes-6","Варианты упаковки в витрине")]),
"kubok-sbera":dict(blocks=[("Задача","Сделать видео, открывающее хоккейный матч на главном экране арены, отсчёт перед началом и ролики для баннеров на самой арене. Обязательное условие: использовать настоящего маскота, кота в джерси."),("Идея","Заказчик дал готовую озвучку. Я написала сценарий под неё, чтобы изображение совпадало с голосом по темпу и смыслу, и построила ролик вокруг маскота."),("Срок","2–3 дня вместе с баннерами. Срочный заказ: ТЗ, все кадры и баннеры для экранов вокруг арены — с нуля."),("Результат","Ролик показали на главном экране арены: он открыл матч. Баннеры крутились на экранах по периметру арены.")],
 steps=[("Озвучка и сценарий","Разметила озвучку по секундам и написала под неё сценарий: кадр под каждую фразу."),("Маскот","Воссоздала кота в джерси так, чтобы он был узнаваем на большом экране."),("Основной ролик и отсчёт","Ролик, открывающий матч, и отсчёт до старта на главном экране арены."),("Баннеры","Сделала зацикленные ролики с хоккеистами для баннеров по периметру арены.")],
 imgs=[("kubok-sbera-3","Основной ролик на главном экране арены"),("kubok-sbera-4","Заставка на главном экране"),("kubok-sbera-1","Баннеры с роликами на фасаде арены"),("kubok-sbera-2","Отсчёт перед началом матча"),("kubok-sbera-5","Кадр из основного ролика"),("kubok-sbera-6","Маскот: кот в джерси")]),
"khl-monopoly":dict(blocks=[("Задача","Рекламный ролик для новой игры «Монополия» совместно с КХЛ. Пожелание заказчика: взять маскотов с упаковки и показать их как настоящих игроков. Нужно было динамичное видео на 15 секунд."),("Идея","Две игры идут одновременно. Маскоты играют в хоккей, а параллельно настоящие люди играют в Монополию. Решающие ходы и победа происходят друг за другом, как будто одно действие продолжает другое."),("Срок","7 дней."),("Результат","15-секундный рекламный ролик нового товара — игры «Монополия» вместе с КХЛ.")],
 steps=[("Сценарий","Ритм на 15 секунд и общая «рифма» между хоккеем и настольной игрой."),("Маскоты","Взяла героев с упаковки и «оживила» их, сохранив узнаваемость."),("Ключевые кадры","Ледовая арена и игровой стол в одном визуальном стиле."),("Видео","Динамичный монтаж двух параллельных линий до общей победы.")],
 imgs=[("khl-monopoly-1","Маскоты на вбрасывании"),("khl-monopoly-5","Решающий момент матча"),("khl-monopoly-3","Бросок кубика: переход к настольной игре"),("khl-monopoly-4","Параллельная игра за столом"),("khl-monopoly-6","Финал: упаковка игры")]),
"zargus":dict(blocks=[("Задача","Показать салон изнутри, подчеркнуть высокое качество изделий и широкий ассортимент."),("Особенность","Главное требование — никаких искажений интерьера и вещей. Нейросетью создан только покупатель, всё остальное настоящее: локации, одежда, фирменный пакет в финале."),("Срок","2 дня."),("Результат","Из реальных фото салона — видео без единого искажения: нейросетью создан только покупатель.")],
 steps=[("Референсы","Реальные фото салона и одежды стали основой."),("Сохранение реальности","Интерьер, вещи и пакет остались точными, нейросеть работала только с героем."),("Герой","Создала покупателя, который естественно взаимодействует с настоящими вещами."),("Видео","Плавное движение по салону без искажений и «плавающих» деталей.")],
 imgs=[("zargus-1","Вход в салон"),("zargus-2","Интерьер салона"),("zargus-3","Покупатель — единственное, что создано нейросетью"),("zargus-4","Фирменный пакет в финале")]),
"yoshida":dict(blocks=[("Задача","Показать чёрную сумку Yoshida & Co с бамбуковыми ручками не в студии, а в жизни: чтобы зритель поверил, что она подходит на любой момент дня."),("Идея","Взять сумку за основу и показать, что она сопровождает девушку весь день: дома, в дороге, на учёбе, на теннисном корте и вечером у моря. Сумка всегда рядом и подходит на все случаи жизни."),("Срок","7 дней."),("Результат","Творческий ролик о дне девушки, разбитом по часам с подписями на японском: 10:30 — лекция, 16:20 — теннис, 18:10 — Дзимботё, 19:29 — море. Сумка в каждой сцене.")],
 steps=[("Сумка","Собрала многоракурсную презентацию сумки: форма, бамбуковые ручки, фактура ткани, внутренние отделения и размер рядом с человеком. Так сумка выглядит одинаково в каждой сцене."),("Героиня","Сделала модельный лист: портреты с разных сторон и детали образа, чтобы лицо и одежда не менялись от кадра к кадру."),("Спортивный образ","Для сцены на корте — отдельный лист с теннисным образом и мудборд."),("Локации","Подобрала места, из которых складывается день: квартира, поезд вдоль моря, метро, кампус, аудитория, теннисный корт, набережная на закате, улица с книжной лавкой."),("Видео","Собрала сцены в одну историю: героиня меняет места и образы, а сумка всё время с ней.")],
 imgs=[("yoshida-1","Сумка: многоракурсная презентация","contain"),("yoshida-2","Лист персонажа: героиня","contain"),("yoshida-3","Теннисный образ и мудборд","contain"),("yoshida-4","Квартира"),("yoshida-5","Поезд вдоль моря"),("yoshida-6","Станция метро"),("yoshida-7","Кампус"),("yoshida-8","Аудитория: сумка рядом"),("yoshida-9","Теннисный корт"),("yoshida-10","Набережная на закате"),("yoshida-11","Улица с книжной лавкой")]),
}

CONTACTS=[("tg","@emblem_a","https://t.me/emblem_a"),("mail","zabuzayera632@gmail.com","mailto:zabuzayera632@gmail.com"),("phone","8\u00a0(916)\u00a0295\u201112\u201142","tel:+79162951242")]

CSP=("default-src 'self'; script-src 'self'"+(" 'unsafe-inline' https://mc.yandex.ru" if METRIKA else "")+"; style-src 'self' 'unsafe-inline'; img-src 'self' data:"+(" https://mc.yandex.ru" if METRIKA else "")+"; media-src 'self'; font-src 'self'; connect-src 'self' https://open.er-api.com"+(" https://mc.yandex.ru" if METRIKA else "")+"; frame-src https://drive.google.com; object-src 'none'; base-uri 'self'; form-action 'none'")
def head(title,desc,path=""):
    ogimg=f'<meta property="og:image" content="{SITE}/assets/og.jpg"><meta name="twitter:card" content="summary_large_image">' if SITE else ''
    ym=('<script>(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym('+METRIKA+',"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true});</script>') if METRIKA else ''
    return f'''<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><meta name="theme-color" content="#EEE7DD">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website"><meta property="og:site_name" content="emblem_a"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:locale" content="ru_RU">{ogimg}
<meta http-equiv="Content-Security-Policy" content="{CSP}"><meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="preload" href="{path}assets/fonts/geologica-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{path}assets/style.css?v=42">{ym}</head><body><svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="marker" x="-15%" y="-15%" width="130%" height="130%"><feTurbulence type="fractalNoise" baseFrequency=".27" numOctaves="2" seed="14" result="g"/><feDisplacementMap in="SourceGraphic" in2="g" scale="3.2" xChannelSelector="R" yChannelSelector="G"/></filter></svg>'''
def nav(cur,p=""):
    L=[("index.html","Главная"),("cases.html","Кейсы"),("prices.html","Цены"),("contacts.html","Контакты")]
    a="".join(f'<a href="{p}{h}"{" aria-current=\"page\"" if h==cur else ""}>{t}</a>' for h,t in L)
    return f'''<header class="nav"><div class="wrap"><a class="logo" href="{p}index.html"><i aria-hidden="true"></i>emblem_a</a>
<!--LANG--><button type="button" class="burger" aria-label="Меню" aria-expanded="false" aria-controls="site-menu">{ico("menu")}</button><nav class="menu" id="site-menu" aria-label="Основное">{a}</nav></div></header>'''
def chips(): return "".join(f'<a class="chip" href="{h}">{ico(i)}{t}</a>' for i,t,h in CONTACTS if i!="tg")
BRIEF="Здравствуйте, Олеся!\n1. Продукт или бренд: \n2. Зачем ролик (продажи, запуск, соцсети, имидж): \n3. Где покажем и какой длины: \n4. Примеры, которые нравятся (ссылки): \n5. Срок и ориентир по бюджету: \nЕсли есть фото товара или логотип — прикреплю."
ABOUT_IMG=('<img src="assets/img/about.jpg" alt="emblem_a" loading="lazy">' if os.path.exists("assets/img/about.jpg") else '<div class="orb" role="img" aria-label="emblem_a"><span>emblem_a</span></div>')
def contact(h="h2"): return f'''<section id="contact" class="contact-sec"><div class="wrap"><div class="contact"><div class="contact-main">
<{h}>Ролик для вашего бренда начинается с одного сообщения</{h}><p>Опишите, что нужно, и я предложу формат ролика, сроки и стоимость. Отвечаю в течение нескольких часов.</p><div class="cta-row"><a class="btn light" href="https://t.me/emblem_a" target="_blank" rel="noopener">{ico("tg")}Написать в Telegram</a><button type="button" class="btn outline-light" data-copy="{BRIEF}" data-done="Скопировано" data-fail="Не получилось скопировать">Скопировать шаблон брифа</button></div><div class="contacts">{chips()}</div></div>
<aside class="contact-aside" aria-labelledby="brief-tips">{sk("plane","sk-contact")}<{"h2" if h=="h1" else "h3"} id="brief-tips">Что написать в первом сообщении</{"h2" if h=="h1" else "h3"}><ol><li>Что нужно показать</li><li>Для какой площадки</li><li>К какому сроку</li></ol></aside></div></div></section>'''
FOOT='<footer><div class="wrap"><div class="foot-row"><span>© 2026 emblem_a</span><span>Видео и визуал на нейросетях</span><span class="foot-links"><a href="{p}contacts.html">Контакты</a><a href="https://t.me/emblem_a" target="_blank" rel="noopener">Telegram</a></span></div></div></footer><script src="{p}assets/lenis.min.js?v=1"></script><script src="{p}assets/main.js?v=42"></script></body></html>'
def foot(p=""): return FOOT.replace("{p}",p)

IMG={"magnit","cakes","khl-monopoly","kubok-sbera","yoshida","vladkon","zargus"}
def thumb(s,p=""):
    return f'<img src="{p}assets/img/{s}.jpg?v=6" alt="" loading="lazy" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">' if s in IMG else ""

def folder(c,href_prefix=""):
    s,t,cat,short,g,tab,did,internal=c
    href=f"{href_prefix}case-{s}.html" if internal else D+did
    ext="" if internal else ' target="_blank" rel="noopener"'
    label="Открыть кейс" if internal else "Смотреть папку"
    return f'''<a class="folder" href="{href}"{ext} data-cat="{cat}"><div class="cover"><div class="art {g}"></div>{thumb(s)}</div>
<div class="txt"><span class="meta br">{cat}</span><h3>{t}</h3><p>{short}</p><span class="go">{label}{ico("ext" if not internal else "arrow")}</span></div></a>'''

DECO={  # name: (viewBox, inner svg)
 "arrow":("0 0 220 200",'<path pathLength="1" d="M 20 150 C 70 60 130 60 150 120 C 165 165 120 190 100 160 M 150 120 L 190 90 M 150 120 L 196 132"/>'),
 "smile":("0 0 200 200",'<path pathLength="1" d="M 100 18 C 48 16 16 58 20 104 C 24 152 64 184 106 182 C 154 180 186 140 182 96 C 178 50 142 20 96 22"/><path pathLength="1" d="M 66 82 L 70 104"/><path pathLength="1" d="M 122 92 C 130 84 142 84 148 92"/><path pathLength="1" d="M 58 128 C 80 156 124 158 146 126"/>'),
 "sparkle":("0 0 200 200",'<path pathLength="1" d="M 80 20 C 84 70 92 80 140 86 C 92 92 84 102 80 150 C 76 102 68 92 20 86 C 68 80 76 70 80 20 Z"/><path pathLength="1" d="M 160 120 C 162 140 166 144 186 146 C 166 148 162 152 160 172 C 158 152 154 148 134 146 C 154 144 158 140 160 120 Z"/>'),
 "underline":("0 0 240 80",'<path pathLength="1" d="M 8 30 C 60 18 140 14 232 24"/><path pathLength="1" d="M 30 54 C 90 42 160 40 220 50"/>'),
 "route":("0 0 240 160",'<path pathLength="1" d="M 10 140 C 40 80 70 140 100 90 C 125 50 150 110 180 70 C 195 50 205 40 222 24 M 222 24 L 196 28 M 222 24 L 218 50"/>'),
 "circle":("0 0 260 120",'<path pathLength="1" d="M 160 14 C 90 4 18 24 14 62 C 10 100 90 114 160 106 C 222 98 252 72 244 44 C 236 18 180 8 120 16"/>'),
 "spiral":("0 0 200 200",'<path pathLength="1" d="M 100 104 C 100 94 114 94 114 106 C 114 122 92 124 88 106 C 82 82 120 74 130 102 C 142 134 104 152 82 134 C 54 112 68 66 106 60 C 154 52 176 98 164 132"/>'),
 "frame":("0 0 220 180",'<path pathLength="1" d="M 20 30 L 200 30 L 200 150 L 20 150 Z"/><path pathLength="1" d="M 20 56 L 200 56 M 20 124 L 200 124"/><path pathLength="1" d="M 40 38 L 40 48 M 66 38 L 66 48 M 92 38 L 92 48 M 118 38 L 118 48 M 144 38 L 144 48 M 170 38 L 170 48 M 40 132 L 40 142 M 66 132 L 66 142 M 92 132 L 92 142 M 118 132 L 118 142 M 144 132 L 144 142 M 170 132 L 170 142"/>'),
 "heart":("0 0 200 180",'<path pathLength="1" d="M 100 160 C 40 120 10 80 30 46 C 50 14 92 24 100 58 C 108 24 150 14 170 46 C 190 80 160 120 100 160"/>'),
 "plane":("0 0 220 180",'<path pathLength="1" d="M 14 84 L 204 18 L 150 160 L 104 104 Z"/><path pathLength="1" d="M 104 104 L 204 18"/><path pathLength="1" d="M 104 104 L 98 150 L 126 126"/>'),
}
def sk(kind,cls): vb,body=DECO[kind]; return f'<svg class="sketch-deco {cls}" viewBox="{vb}" aria-hidden="true"><g filter="url(#marker)">{body}</g></svg>'
# reviews rebuilt from the Telegram screenshots: text is verbatim, names are left out.
# message: (side, kind, text, time, reaction)  side: me | cl ; kind: text | file | day | fwd
REVIEWS=[
 ("review-6",[("me","file","32.9 МБ","7:11 PM",""),("cl","text","Ну Всё! Получилось как и не мечталось! Всем Вам огромное Спасибо! Ожидаю счёта и потом файл.","7:16 PM","")]),
 ("review-5",[("cl","fwd","","",""),("cl","text","Очень понравилось! Я в восторге просто 🙏","11:35 AM",""),("cl","text","И Лесе передайте благодарность 🙏","11:35 AM",""),("cl","text","Здорово получилось 👍👍👍","11:35 AM","")]),
 ("review-3",[("me","file","32.9 МБ","7:35 PM","🙏"),("cl","text","Скорость наше все ) директору понравилось","7:42 PM",""),("me","text","Рада это слышать 🙏","7:43 PM","")]),
 ("review-4",[("me","file","29.8 МБ","1:18 PM",""),("me","text","Добрый день, второе видео","1:18 PM",""),("cl","text","Ой мне все нравится. Такой хорошенький он, прям прелесть!","1:23 PM",""),("cl","text","Спасибо, Леся!","1:25 PM","")]),
 ("review-2",[("me","text","Если по видео всё хорошо, отправлю файлом, чтобы качество было получше","9:29 AM",""),("cl","text","Да супер просто 🔥🔥🔥🔥","9:46 AM","")]),
 ("review-1",[("me","file","25.6 МБ","3:11 PM","🔥"),("me","text","Немного сокращённый вариант, чтобы не так затянуто было, и подправила переход","3:11 PM",""),("me","day","23 марта","",""),("cl","text","Доброе утро! Отличная работа 🔥","7:11 AM",""),("me","text","Благодарю 🙏","7:30 AM","")]),
]
def chat(img,msgs):
    out=[]
    for side,kind,text,time,react in msgs:
        if kind=="day": out.append(f'<li class="m-day">{text}</li>'); continue
        if kind=="fwd": out.append('<li class="m-fwd">Переслано от клиента</li>'); continue
        who='<span class="sr">Олеся: </span>' if side=="me" else '<span class="sr">Клиент: </span>'
        meta=f'<span class="m-time">{time}{" ✓✓" if side=="me" else ""}</span>'
        rx=f'<span class="m-react"><span class="sr">реакция: </span>{react}</span>' if react else ""
        if kind=="file":
            body=f'<span class="m-file"><span class="m-play" aria-hidden="true">▶</span><span><b>Видео</b><small>{text}</small></span></span>'
        else:
            body=f'<span class="m-text">{text}</span>'
        out.append(f'<li class="m {"out" if side=="me" else "in"}">{who}{body}{rx}{meta}</li>')
    return f'''<li><figure class="chat"><figcaption><span class="chat-src">Переписка в Telegram</span><a class="rv-orig" href="assets/img/reviews/{img}.jpg">Оригинал</a></figcaption><ol class="msgs">{"".join(out)}</ol></figure></li>'''
def reviews():
    return f'''<section id="reviews" class="reviews"><div class="wrap">
<div class="rv-head">{sk("heart","sk-reviews")}<h2>Что говорят клиенты</h2><blockquote class="rv-quote">«Получилось как и не мечталось!»</blockquote></div>
<ul class="rv-wall">{"".join(chat(i,m) for i,m in REVIEWS)}</ul>
<dialog class="rv-dialog" aria-labelledby="rv-dlg-t"><h2 id="rv-dlg-t" class="sr">Оригинал отзыва</h2><button type="button" class="rv-close" aria-label="Закрыть">×</button></dialog>
</div></section>
'''
PK=[('film', 'Видео для карточки товара', 'До 15 секунд. Товар в движении, красивый свет, 1–4 сцены. Подходит для маркетплейсов и сторис.', 'от 5 000 ₽', 'до 4 дней'), ('spark', 'Рекламный ролик', '15–30 секунд. Сценарий, несколько сцен, монтаж, музыка. Для таргета, соцсетей и сайта.', 'от 10 000 ₽', 'до 5 дней'), ('layers', 'Ролик с историей', '30–60 секунд. Сюжет с героями, раскадровка, один персонаж во всех сценах, озвучка по желанию. Для имиджевой рекламы и презентаций.', 'от 15 000 ₽', 'до 8–10 дней'), ('wand', 'AI-фото для бренда', 'Статичные кадры: товар в интерьере, на модели, в рекламной сцене.', 'от 1 000 ₽ за кадр', 'пакет из 10 кадров от 10 000 ₽'), ('layers', 'Контент на месяц', 'Регулярные ролики и фото для соцсетей и рекламы: план на месяц, единый стиль, один герой во всех роликах.', 'по запросу', '4–8 роликов в месяц')]
EX=[('Адаптация под другой формат (вертикаль, квадрат, горизонталь)', 'от 2 000 ₽'), ('Озвучка AI-голосом', 'от 2 000 ₽'), ('Озвучка профессиональным диктором', 'от 5 000 ₽'), ('Дополнительный круг правок сверх включённых', 'от 2 000 ₽'), ('Срочное выполнение', '+30% к стоимости')]
ST=[('Разбор задачи', 'Перед стартом я выясняю, для чего нужен ролик: продать товар в карточке, привлечь заявки из рекламы, рассказать о бренде. От этого зависит всё: длина, темп, какие кадры показать первыми, где поставить логотип. Ролик, сделанный без понимания цели, может быть красивым, но бесполезным для продаж.'), ('Идея и сценарий', 'Придумываю, как показать ваш продукт так, чтобы его запомнили. Пишу сценарий по сценам: что происходит, где, с кем, какое настроение. Например, для конфет это не просто «конфета на столе», а конфеты, которые растут на цветущем дереве. Хорошая идея стоит дороже любой нейросети.'), ('Раскадровка и ключевые кадры', 'Прежде чем делать видео, создаю статичные кадры каждой сцены и показываю их вам. На этом этапе можно поменять героя, свет, цвет упаковки или место действия. Это экономит ваше время и деньги: правки на картинках занимают минуты, а переделка готового видео — дни.'), ('Генерация и отбор', 'Нейросеть не выдаёт идеальный результат с первого раза. Чтобы получить одну удачную сцену, приходится делать много попыток и отбрасывать брак: искажённые руки, лишние пальцы, «плывущие» лица, нечитаемые надписи, неестественные движения. Вы видите только лучшие кадры, а за ними стоят часы отбора.'), ('Один герой и один товар во всех кадрах', 'Самая сложная часть работы. Нейросеть каждый раз рисует немного по-другому: у героя меняется лицо, у упаковки цвет, у логотипа форма. Я слежу, чтобы от первой до последней сцены всё выглядело одинаково и узнаваемо. Именно это отличает рекламный ролик от набора случайных красивых картинок.'), ('Монтаж, звук и цвет', 'Собираю сцены в цельную историю с правильным ритмом. Подбираю музыку и звуки, выравниваю цвет между кадрами, чтобы ролик выглядел как одна съёмка. Добавляю текст, логотип и призыв к действию.'), ('Адаптация под площадки', 'Подготавливаю файлы под требования площадок: размер, формат, длительность, вес. Ролик сразу можно загружать в карточку маркетплейса, рекламный кабинет или соцсети без доработок.'), ('Профессиональные нейросети', 'Для реалистичного результата я использую платные профессиональные сервисы. Каждая попытка генерации в них стоит денег, а попыток на один ролик требуется много. Эти расходы уже включены в цену, вам не нужно ничего оплачивать отдельно.'), ('Правки и права', 'В стоимость входят два круга правок, чтобы результат точно совпал с вашими ожиданиями. После оплаты вы получаете право использовать ролик в рекламе, на сайте и в соцсетях.')]
pcards="".join(f'<div class="pkg"><div class="pkg-main"><h3>{t}</h3><p>{d}</p></div><div class="price">{sk("circle","sk-price") if n==0 else ""}<b>{p}</b><span>{s}</span></div></div>' for n,(i,t,d,p,s) in enumerate(PK))
exl="".join(f'<li><span>{a}</span><b>{p}</b></li>' for a,p in EX)
stl="".join(f'<div class="step"><div><h3>{a}</h3><p>{c}</p></div></div>' for a,c in ST)

FAQ=[("Сколько времени занимает ролик?","Видео для карточки товара — до 4 дней, рекламный ролик — до 5 дней, ролик с историей — до 8–10 дней. Срочное выполнение: +30% к стоимости."),
("Сколько правок входит в стоимость?","Два круга правок. Дополнительный круг — от 2 000 ₽."),
("Могу ли я использовать ролик в рекламе?","Да. После оплаты вы получаете право использовать ролик в рекламе, на сайте и в соцсетях."),
("Нужно ли отдельно платить за нейросети?","Нет. Расходы на профессиональные сервисы уже включены в цену."),
("Можно ли получить ролик в разных форматах?","Да: вертикальный, квадратный и горизонтальный. Адаптация под другой формат — от 2 000 ₽."),
("Можно ли использовать реальный товар или упаковку?","Да. Реальные фото товара, упаковки и интерьера я беру за основу, чтобы они выглядели точно, как в жизни."),
("С чего начать?","Напишите в Telegram: что нужно показать, для какой площадки и к какому сроку. Я предложу формат, сроки и стоимость. Отвечаю в течение нескольких часов.")]
faqs="".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQ)

# ---------- index
SKETCH=[
 '<path d="M 30 50 L 190 50 L 190 210 L 30 210 Z M 30 80 L 190 80 M 30 180 L 190 180 M 52 58 L 52 72 M 80 58 L 80 72 M 108 58 L 108 72 M 136 58 L 136 72 M 164 58 L 164 72 M 52 188 L 52 202 M 80 188 L 80 202 M 108 188 L 108 202 M 136 188 L 136 202 M 164 188 L 164 202"/>',
 '<path d="M 70 50 L 180 130 L 70 210 Z"/><path d="M 30 40 C 20 90 20 170 30 220"/>',
 '<path d="M 110 130 C 110 118 126 118 126 132 C 126 150 100 152 96 132 C 90 104 132 96 142 126 C 154 162 112 182 88 160 C 60 134 74 84 116 78 C 168 70 190 120 176 158"/>',
]
def reelcard(c,i=0):
    s,t,cat,short,g,tab,did,internal=c
    sk=f'<svg class="sketch s{i%3}" viewBox="0 0 220 260" aria-hidden="true"><g filter="url(#marker)">{SKETCH[i%3]}</g></svg>'
    return f'<a class="reel-card" href="case-{s}.html"><div class="media"><div class="art {g}"></div>{thumb(s)}</div>{sk}<div class="cap"><div><span class="br">{cat}</span><h3>{t}</h3></div><span class="go">Открыть кейс{ico("arrow")}</span></div></a>'
def fly(cls,slug,title,tag,media,r,k):
    return f'<a class="fly {cls}" href="case-{slug}.html" style="--r:{r}deg;--k:{k}" aria-label="{tag}: {title}">{media}<span class="tag">{tag}</span></a>'
def vid(n,poster): return f'<video src="assets/video/hero-{n}.mp4?v=3" poster="{poster}" autoplay muted loop playsinline preload="metadata" aria-hidden="true"></video>'
def pic(n): return f'<img src="assets/img/{n}.jpg?v=6" alt="" loading="eager">'
flies=(fly("p1","khl-monopoly","КХЛ Монополия","Реклама",vid("khl-monopoly","assets/img/khl-monopoly.jpg"),-6,1.6)
 +fly("p2","magnit","Магнит — лучший наставник","Бренды",pic("magnit"),4,-1)
 +fly("p3","kubok-sbera","Кубок Сбера по хоккею","Спорт",pic("kubok-sbera"),-3,.8)
 +fly("p4","yoshida","Yoshida & Co","Yoshida & Co",vid("yoshida","assets/img/yoshida-hero.jpg"),5,-1.4)
 +fly("p5","cakes","Реклама упаковки для десертов","Для товаров",vid("cakes","assets/img/cakes-hero.jpg?v=6"),-4,1.1)
 +fly("p6","vladkon","Владкон — конфеты на цветущем дереве","Бренды",pic("vladkon"),3,-.7))
hero=f'''<main><section class="intro">
<div class="wrap intro-top"><span class="br">Олеся — AI-креатор</span><span class="br">Видео и визуал на нейросетях</span></div>
<div class="scene"><figure class="me"><img src="assets/img/about.jpg" alt="emblem_a" width="800" height="1200" fetchpriority="high"></figure><p class="wordmark" aria-hidden="true">emblem_a</p>{flies}</div>
<div class="wrap intro-bottom"><h1>Реалистичные ролики без съёмочной команды</h1>
<div><p class="lead">Создаю рекламные ролики и визуал для брендов с помощью нейросетей. Выглядит как профессиональная съёмка, а стоит дешевле и готово быстрее.</p>
{sk("arrow","sk-hero")}<div class="cta-row"><a class="btn primary" href="cases.html">Смотреть кейсы {ico("arrow")}</a><a class="btn ghost" href="https://t.me/emblem_a" target="_blank" rel="noopener">Написать в Telegram</a></div></div></div>
</section>
<section id="about"><div class="wrap about"><figure class="about-photo">{sk("smile","sk-about")}<img src="assets/img/about-2.jpg" alt="Олеся, emblem_a" loading="lazy" width="800" height="1000"></figure><div class="about-text"><h2>Привет, я Олеся</h2>
<p class="lead">AI-креатор. Делаю рекламные ролики, которые выглядят как настоящая съёмка.</p>
<p>В нейросети я пришла из UI/UX-дизайна и монтажа. Поэтому думаю не только о красивой картинке, но и о том, что зритель увидит первым и что запомнит.</p>
<p>Больше всего люблю коммерческий реализм. Любимой категории товаров нет: в каждом бренде ищу его историю и то, чем он отличается от других.</p>
<p class="fav"><b>Любимый проект — <a class="inline" href="case-kubok-sbera.html">«Кубок Сбера по хоккею»</a>.</b> Срочный заказ на 2–3 дня: у меня была только озвучка, а сценарий, все кадры и баннеры для экранов арены я придумала с нуля.</p>
<ul class="about-facts"><li><b>~2 года</b> в AI-видео</li><li><b>50+</b> роликов</li><li><b>20+</b> брендов, среди них Магнит, Кубок Сбера и КХЛ</li><li><b>Удалённо</b> работаю с клиентами из России и других стран</li><li><b>За несколько часов</b> отвечаю на сообщения</li></ul>
<p class="also">Ещё делаю <a class="inline" href="prices.html#web">сайты, приложения и AI-агентов →</a></p>
<a class="btn primary" href="https://t.me/emblem_a" target="_blank" rel="noopener">Написать в Telegram</a></div></div></section>
<section id="skills"><div class="wrap split"><div class="split-head"><h2>Что вы получаете</h2>{sk("sparkle","sk-skills")}</div>
<ul class="rows">
<li><h3>Реалистичное видео на нейросетях</h3><p>Ролики, которые выглядят как настоящая съёмка: живой свет, фактура материалов, движение камеры. Работаю на новейших нейросетях для видео.</p></li>
<li><h3>Герой и товар не меняются от кадра к кадру</h3><p>Персонаж или товар выглядит одинаково от первой до последней сцены, без искажений лица и деталей.</p></li>
<li><h3>Сценарий и режиссура</h3><p>Придумываю идею, пишу сценарий, делаю раскадровку. Отталкиваюсь от задачи бизнеса, а не просто от красивой картинки.</p></li>
<li><h3>Видео для товаров</h3><p>Упаковка, косметика, одежда, украшения. Ролики для карточек маркетплейсов и рекламы.</p></li>
<li><h3>Быстрые правки</h3><p>Вношу правки и делаю новые версии за часы, а не недели. Удобно, когда нужно проверить несколько вариантов рекламы.</p></li>
<li><h3>Права на ролик</h3><p>После оплаты вы получаете право использовать ролик в рекламе, на сайте и в соцсетях.</p></li>
</ul></div></section>
<section id="cases" class="reel"><div class="reel-pin">
<div class="wrap reel-head"><h2>Проекты для брендов</h2><div class="reel-links"><a class="reel-skip" href="cases.html">Все кейсы {ico("arrow")}</a><a class="reel-jump" href="#why">Пропустить ↘</a></div></div>
<div class="reel-stage">{"".join(reelcard(c,i) for i,c in enumerate(C))}</div>
<div class="wrap reel-foot"><div class="reel-count" aria-hidden="true"><b class="rc-cur">01</b><span class="rc-bar"><i></i></span><span>{len(C):02d}</span></div><span class="reel-hint">Листайте, чтобы посмотреть проекты</span><div class="reel-nav"><button type="button" class="reel-btn" data-dir="-1" aria-label="Предыдущий проект">{ico("arrow","ico flip")}</button><button type="button" class="reel-btn" data-dir="1" aria-label="Следующий проект">{ico("arrow")}</button></div></div>
</div></section>
{reviews()}<section id="why" class="dark-sec"><div class="wrap"><div class="split"><div class="split-head"><h2>Почему брендам нужен контент на нейросетях</h2><p class="lead">Тот же результат, что после съёмки, только быстрее, дешевле и без аренды студии, актёров и съёмочной группы.</p></div>
<ul class="rows">
<li><h3>Быстро</h3><p>Ролик, который раньше готовили месяц, я делаю за несколько дней. Вы успеваете выйти с рекламой, пока тема ещё на пике.</p></li>
<li><h3>Выгодно</h3><p>Не нужно платить за студию, свет, актёров и съёмочную группу. Деньги идут на рекламу, а не на производство.</p></li>
<li><h3>Под все площадки сразу</h3><p>Один ролик превращается в набор: вертикальное видео для соцсетей, баннер, карточка для маркетплейса. Без дополнительных съёмок.</p></li>
</ul></div>
<blockquote class="pull">{sk("underline","sk-pull")}<span>Нейросеть — это инструмент, а не автор.</span> Идею, сценарий и финальную проверку качества я делаю сама, а технология помогает сделать это быстрее.</blockquote></div></section>
<section id="process"><div class="wrap"><div class="head">{sk("route","sk-process")}<h2>Как проходит работа</h2><p class="lead">От брифа до готового файла — шесть шагов. Ключевые кадры вы согласовываете до начала работы с видео.</p></div>
<ol class="process">
<li><h3>Разбор задачи</h3><p>Выясняю, для чего нужен ролик: продать товар, привлечь заявки или рассказать о бренде. От этого зависят длина, темп и первые кадры.</p></li>
<li><h3>Идея и сценарий</h3><p>Придумываю, как показать продукт так, чтобы его запомнили, и пишу сценарий по сценам.</p></li>
<li><h3>Ключевые кадры</h3><p>Делаю статичные кадры каждой сцены и согласовываю их с вами до того, как делать видео. Правки на этом этапе занимают минуты.</p></li>
<li><h3>Генерация и отбор</h3><p>Делаю много попыток, отбираю удачные и слежу, чтобы герой и товар выглядели одинаково во всех сценах.</p></li>
<li><h3>Монтаж и звук</h3><p>Собираю сцены в цельную историю: ритм, музыка, цвет, текст и логотип.</p></li>
<li><h3>Правки и сдача</h3><p>Два круга правок входят в стоимость. Готовый файл — в нужном формате под вашу площадку.</p></li>
</ol></div></section>
<section id="pricing"><div class="wrap"><div class="head"><h2>Сколько стоит ролик</h2><p class="lead">Ориентиры по стоимости. Точную цену назову после короткого брифа.</p></div>
<div class="pricelist">{pcards}</div>
<p class="section-cta"><a class="btn ghost" href="prices.html">Все цены и условия {ico("arrow")}</a></p><!--USDNOTE--></div></section>
<section id="faq"><div class="wrap split"><div class="split-head"><h2>Частые вопросы</h2></div>
<div class="faqlist">{faqs}</div></div></section>
{contact()}</main>'''
W("index.html",head("emblem_a — рекламные ролики на нейросетях для брендов","Портфолио AI-креатора: реалистичные рекламные видео и визуал на нейросетях.")+nav("index.html")+hero+foot())

# ---------- cases
body=f'''<main><section style="padding-top:48px"><div class="wrap"><div class="head">{sk("frame","sk-pagehead")}<h1 >Проекты для брендов</h1><p class="lead">Семь проектов: у каждого — описание того, как проходила работа.</p></div><div class="folders">{"".join(folder(c) for c in C)}</div></div></section>{contact()}</main>'''
W("cases.html",head("Кейсы — emblem_a","Все проекты AI-креатора")+nav("cases.html")+body+foot())

def player(s,g):
    if s in VID:
        return f'<div class="player"><iframe src="https://drive.google.com/file/d/{VID[s]}/preview" title="Видео проекта" allow="autoplay; fullscreen" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe></div>'
    return f'<div class="player"><div class="art {g}" style="position:absolute;inset:0"></div><span class="play" style="width:88px;height:88px;margin:-44px">{ico("play")}</span></div>'

# ---------- contacts
cpage=f'''<main class="contacts-page">{contact("h1")}
<section id="faq"><div class="wrap split"><div class="split-head"><h2>Частые вопросы</h2>{sk("sparkle","sk-faq")}</div>
<div class="faqlist">{faqs}</div></div></section></main>'''
W("contacts.html",head("Контакты — emblem_a","Как связаться с emblem_a: Telegram, почта и телефон")+nav("contacts.html")+cpage+foot())
nf=f'''<main><section class="notfound"><div class="wrap">{sk("spiral","sk-404")}<h1>Такой страницы нет</h1><p class="lead">Возможно, ссылка устарела. Начните с главной или посмотрите кейсы.</p><div class="cta-row"><a class="btn primary" href="{BASE}index.html">На главную</a><a class="btn ghost" href="{BASE}cases.html">Кейсы</a></div></div></section></main>'''
W("404.html",head("Страница не найдена — emblem_a","Такой страницы нет",BASE)+nav("",BASE)+nf+foot(BASE))

# ---------- prices
prices=f'''<main><section style="padding-bottom:40px"><div class="wrap"><div class="head"><h1 >Сколько стоит ролик</h1><p class="lead">Итоговая цена зависит от длины ролика, сложности сцен и количества версий. Ниже ориентиры, точную стоимость назову после короткого брифа.</p></div>
<div class="pricelist">{pcards}</div>
<div class="extras">{sk("arrow","sk-extras")}<h3>Дополнительно</h3><ul>{exl}</ul></div>
<div class="incl">{ico("check")}<p><b>В каждый пакет входит:</b> 2 круга правок, согласование ключевых кадров до начала работы с видео, готовый файл в нужном формате, права на использование ролика в рекламе.</p></div>
<div class="extras" id="web"><h3>Сайты, приложения и AI-агенты</h3><p class="note">Кроме роликов, делаю цифровые продукты: от дизайна до запуска. Цены — ориентир, точную назову после брифа.</p><ul><li><span>Лендинг: дизайн и сборка одной страницы</span><b>от 40 000 ₽</b></li><li><span>Многостраничный сайт</span><b>от 80 000 ₽</b></li><li><span>AI-агент или чат-бот для бизнеса: ответы клиентам, приём заявок, интеграции</span><b>от 50 000 ₽</b></li><li><span>Веб- или мобильное приложение</span><b>по запросу</b></li></ul><p class="note">Расходы на нейросети и хостинг для AI-агентов считаются отдельно.</p></div><!--USDNOTE--></div></section>
<section class="dark-sec"><div class="wrap"><div class="head">{sk("spiral","sk-dark")}<h2>За что вы платите</h2><p class="lead">Нейросеть не делает рекламу по одной кнопке. Готовый ролик — это несколько дней работы, десятки попыток и много ручного контроля. Вот из чего складывается цена.</p></div><div class="steps dark">{stl}</div></div></section>
<section><div class="wrap"><div class="vs">{sk("heart","sk-vs")}<h2 style="margin:14px 0 18px">А если снимать по-настоящему?</h2><p>Для съёмки даже короткого рекламного ролика нужно арендовать студию и технику, пригласить оператора, актёров, визажиста, а потом смонтировать материал. Только это обычно стоит от 50 000 ₽, и пересъёмка оплачивается заново. В AI-ролике новая сцена или другой герой — это правка, а не ещё один съёмочный день.</p></div>
<div class="pull light"><span>Вы платите не за нажатие кнопки, а за идею, контроль качества и десятки часов отбора,</span> чтобы ролик выглядел как настоящая съёмка и работал на продажи.</div></div></section>{contact()}</main>'''
W("prices.html",head("Цены — emblem_a","Сколько стоит AI-ролик: пакеты, дополнительные услуги и из чего складывается цена")+nav("prices.html")+prices+foot())

# ---------- case pages
main=C
for i,c in enumerate(main):
    s,t,cat,short,g,tab,did,_=c
    prev=main[i-1]; nxt=main[(i+1)%len(main)]
    d=CASES[s]
    blocks="".join(f'<div class="card"><span class="br">{h}</span><p style="color:var(--ink);font-size:var(--t-lead);margin-top:14px">{p}</p></div>' for h,p in d["blocks"])
    st="".join(f'<div class="step"><div><h3>{a}</h3><p>{p}</p></div></div>' for a,p in d["steps"])
    figs="".join(f'<figure class="shot"><div class="ph {("contain" if len(x)>2 else "")}"><img src="assets/img/cases/{x[0]}.jpg?v=9" alt="{x[1]}" loading="lazy"></div><figcaption>{x[1]}</figcaption></figure>' for x in d["imgs"])
    ep=""
    if d.get("epochs"):
        items="".join(f'<div class="ep"><h3>{a}</h3>'+(f'<p>{c}</p>' if c else '')+'</div>' for a,c in d["epochs"])
        ep=f'<section style="padding:56px 0 0"><div class="wrap"><div class="head"><h2>Шесть эпох передачи опыта</h2></div><div class="epochs">{items}</div></div></section>'
    note=f'<p class="gnote">{d["note"]}</p>' if d.get("note") else ""
    html=f'''<main><section class="case-hero"><div class="wrap"><div class="crumbs"><a href="cases.html">Кейсы</a><span>/</span><span>{t}</span></div>
<div class="case-title">{sk("sparkle" if i%2 else "spiral","sk-casehead")}<h1>{t}</h1></div><p class="lead">{short}</p>
{player(s,g)}
<p style="margin-top:22px"><a class="btn primary" href="{D+did}" target="_blank" rel="noopener">Смотреть все материалы {ico("ext")}</a></p></div></section>
<section style="padding:32px 0 8px"><div class="wrap"><div class="grid2">{blocks}</div></div></section>
{ep}<section style="padding-top:56px"><div class="wrap"><div class="head">{sk("route","sk-process")}<h2>Этапы работы</h2></div><div class="steps">{st}</div></div></section>
<section style="padding-top:20px"><div class="wrap"><div class="head">{sk("frame","sk-gallery")}<h2>Кадры проекта</h2>{note}</div><div class="gallery">{figs}</div></div></section>
<section class="case-cta-sec"><div class="wrap"><div class="case-cta">{sk("arrow","sk-cta")}<div><h2>Хотите похожий ролик для своего бренда?</h2><p>Напишите, что нужно показать, — предложу формат, сроки и стоимость.</p></div><a class="btn primary" href="https://t.me/emblem_a" target="_blank" rel="noopener">{ico("tg")}Обсудить в Telegram</a></div></div></section>
<section style="padding:0 0 40px"><div class="wrap pager"><a class="btn ghost" href="case-{prev[0]}.html">← {prev[1]}</a><a class="btn ghost" href="case-{nxt[0]}.html">{nxt[1]} →</a></div></section></main>'''
    W(f"case-{s}.html",head(f"{t} — emblem_a",short)+nav("cases.html")+html+foot())
open(os.path.join(OUT,".htaccess"),"w").write("""# emblem_a — settings for Apache hosting (Beget, Timeweb, REG.RU)
AddDefaultCharset utf-8
ErrorDocument 404 /404.html
Options -Indexes

<IfModule mod_rewrite.c>
  RewriteEngine On
  # always open the site over HTTPS
  RewriteCond %{HTTPS} off
  RewriteCond %{HTTP:X-Forwarded-Proto} !https
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
  # www -> without www
  RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
  RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
</IfModule>

<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "DENY"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
  Header always set Strict-Transport-Security "max-age=31536000"
  Header always set Content-Security-Policy "frame-ancestors 'none'"
  # pages are always fresh; files with ?v= in the link can be cached for a long time
  <FilesMatch "\\.html$">
    Header set Cache-Control "no-cache"
  </FilesMatch>
  <FilesMatch "\\.(css|js|woff2|jpg|png|svg|mp4)$">
    Header set Cache-Control "public, max-age=31536000"
  </FilesMatch>
</IfModule>

<IfModule mod_mime.c>
  AddType font/woff2 .woff2
  AddType video/mp4 .mp4
</IfModule>
""")
open(os.path.join(OUT,"robots.txt"),"w").write("User-agent: *\nAllow: /\n"+(f"Sitemap: {SITE}/sitemap.xml\n" if SITE else ""))
if SITE:
    pages=["index.html","cases.html","prices.html","contacts.html"]+[f"case-{c[0]}.html" for c in C]
    u="".join(f'<url><loc>{SITE}/{n}</loc><xhtml:link rel="alternate" hreflang="ru" href="{SITE}/{n}"/><xhtml:link rel="alternate" hreflang="en" href="{SITE}/en/{n}"/></url><url><loc>{SITE}/en/{n}</loc><xhtml:link rel="alternate" hreflang="ru" href="{SITE}/{n}"/><xhtml:link rel="alternate" hreflang="en" href="{SITE}/en/{n}"/></url>' for n in pages)
    open(os.path.join(OUT,"sitemap.xml"),"w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{u}</urlset>')
# ready-to-upload archive: everything inside dist/, including the hidden .htaccess
import zipfile
with zipfile.ZipFile("emblem_a-site.zip","w",zipfile.ZIP_DEFLATED) as z:
    for root,_,files in os.walk(OUT):
        for fn in files:
            if fn==".DS_Store": continue
            full=os.path.join(root,fn); z.write(full,os.path.relpath(full,OUT))
print("ok — site in dist/, archive emblem_a-site.zip"+("" if SITE else "  (SITE is empty: set your domain at the top of build.py before publishing)"))
