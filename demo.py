from courier_delivery.value_objects import Weight, WeightDC
from courier_delivery.entities import Parcel
from courier_delivery.route import Route, ParcelNotFound
 
 
def demo_weight() -> None:
    print("=== 1. Два різні екземпляри з однаковим вмістом ===")
    a = Weight(500)
    b = Weight(500)
    print(f"a = {a!r}, b = {b!r}")
    print(f"a is b -> {a is b}")   # False: різні об'єкти в пам'яті
    print(f"a == b -> {a == b}")   # True: рівність за вмістом полів
    print()
 
    print("=== 2. Weight як елемент set і ключ dict ===")
    weights_set = {Weight(200), Weight(500), Weight(500), Weight(1000)}
    print(f"set містить {len(weights_set)} унікальних ваг (500 г продублювався)")
    for w in sorted(weights_set):
        print(f"  {w}")
 
    prices_by_weight = {
        Weight(200): 40,
        Weight(500): 60,
        Weight(1000): 90,
    }
    lookup = Weight(500)
    print(f"Ціна для {lookup} = {prices_by_weight[lookup]} грн")
    print()
 
    print("=== 3. Сортування списку об'єктів-значень ===")
    parcels_weights = [Weight(1500), Weight(300), Weight(800), Weight(50)]
    print("До сортування: ", [str(w) for w in parcels_weights])
    print("Після sorted():", [str(w) for w in sorted(parcels_weights)])
    print()
 
    print("=== 4. Спроба змінити поле незмінного об'єкта ===")
    frozen_weight = Weight(750)
    try:
        frozen_weight.grams = 800
    except AttributeError as exc:
        print(f"Перехоплено AttributeError: {exc}")
 
    try:
        frozen_weight.extra_field = "щось нове"
    except AttributeError as exc:
        print(f"Перехоплено AttributeError (новий атрибут): {exc}")
    print()
 
    print("=== 5. Те саме, але для dataclass-варіанту WeightDC ===")
    dc1 = WeightDC(500)
    dc2 = WeightDC(500)
    print(f"dc1 = {dc1!r}, dc1 == dc2 -> {dc1 == dc2}, dc1 is dc2 -> {dc1 is dc2}")
    try:
        dc1.grams = 999
    except AttributeError as exc:
        print(f"Перехоплено AttributeError: {exc}")
 
 
def demo_parcel() -> None:
    print("=== 1. Створення коректної сутності Parcel ===")
    p = Parcel(tracking="UA-123456", weight=1500, dest_city="Kyiv", cost=120)
    print(p)
    print()
 
    print("=== 2. Некоректні значення: tracking ===")
    try:
        Parcel(tracking="bad-format", weight=1500, dest_city="Kyiv", cost=120)
    except ValueError as exc:
        print(f"Конструктор, перехоплено ValueError: {exc}")
    try:
        p.tracking = ""
    except ValueError as exc:
        print(f"Присвоєння, перехоплено ValueError: {exc}")
    print()
 
    print("=== 3. Некоректні значення: weight (поза діапазоном 1..30000) ===")
    try:
        Parcel(tracking="UA-123456", weight=-5, dest_city="Kyiv", cost=120)
    except ValueError as exc:
        print(f"Конструктор, перехоплено ValueError: {exc}")
    try:
        p.weight = 50000
    except ValueError as exc:
        print(f"Присвоєння, перехоплено ValueError: {exc}")
    print()
 
    print("=== 4. Некоректні значення: dest_city (порожній рядок) ===")
    try:
        Parcel(tracking="UA-123456", weight=1500, dest_city="   ", cost=120)
    except ValueError as exc:
        print(f"Конструктор, перехоплено ValueError: {exc}")
    try:
        p.dest_city = ""
    except ValueError as exc:
        print(f"Присвоєння, перехоплено ValueError: {exc}")
    print()
 
    print("=== 5. Некоректні значення: cost (не додатне) ===")
    try:
        Parcel(tracking="UA-123456", weight=1500, dest_city="Kyiv", cost=0)
    except ValueError as exc:
        print(f"Конструктор, перехоплено ValueError: {exc}")
    try:
        p.cost = -10
    except ValueError as exc:
        print(f"Присвоєння, перехоплено ValueError: {exc}")
    print()
 
    print("=== 6. Parcel.from_dict на коректному словнику ===")
    good_data = {"tracking": "KY-000123A", "weight": 2300, "dest_city": "Odesa", "cost": 95}
    p2 = Parcel.from_dict(good_data)
    print(p2)
    print()
 
    print("=== 7. Parcel.from_dict на некоректному словнику ===")
    bad_data = {"tracking": "KY-000123A", "weight": 40000, "dest_city": "Odesa", "cost": 95}
    try:
        Parcel.from_dict(bad_data)
    except ValueError as exc:
        print(f"from_dict, перехоплено ValueError: {exc}")
    print()
 
    print("=== 8. Статичний метод is_valid_tracking ===")
    print(f"is_valid_tracking('UA-123456')  -> {Parcel.is_valid_tracking('UA-123456')}")
    print(f"is_valid_tracking('bad-format') -> {Parcel.is_valid_tracking('bad-format')}")
 
 
def build_demo_route() -> Route:
    parcels = [
        Parcel(tracking="UA-100001", weight=500, dest_city="Kyiv", cost=50),
        Parcel(tracking="UA-100002", weight=1200, dest_city="Lviv", cost=80),
        Parcel(tracking="UA-100003", weight=3000, dest_city="Kyiv", cost=120),
        Parcel(tracking="UA-100004", weight=15000, dest_city="Odesa", cost=300),
        Parcel(tracking="UA-100005", weight=900, dest_city="Kyiv", cost=70),
    ]
    return Route(parcels)
 
 
def demo_route() -> None:
    route = build_demo_route()
 
    print("=== 1. Протокол послідовності (3.1) ===")
    print(f"len(route) -> {len(route)}")
    print(f"route[0] -> {route[0]}")
 
    sliced = route[0:2]
    print(f"route[0:2] -> {sliced}")
    print(f"type(route[0:2]) -> {type(sliced)}")  # саме Route, а не list
 
    second_parcel = route[1]
    print(f"route[1] in route -> {second_parcel in route}")
    print(f"'UA-100002' in route -> {'UA-100002' in route}")
    print(f"'ZZ-000000' in route -> {'ZZ-000000' in route}")
 
    print("Обхід у циклі for:")
    for parcel in route:
        print(f"  {parcel.tracking} -> {parcel.dest_city}, {parcel.weight}")
    print()
 
    print("=== 2. Посторінковий обхід (3.2) ===")
    # 5 елементів, по 2 на сторінку -> остання сторінка неповна (1 елемент)
    for page_number, page in enumerate(route.pages(2), start=1):
        print(f"Сторінка {page_number}: {[p.tracking for p in page]}")
    print()
 
    print("=== 3. Запит через виклик як функції (3.3) ===")
    kyiv_only = route(city="Kyiv")
    print(f"route(city='Kyiv') -> {[p.tracking for p in kyiv_only]}")
 
    light_parcels = route(weight_max=1000)
    print(f"route(weight_max=1000) -> {[p.tracking for p in light_parcels]}")
 
    kyiv_light = route(city="Kyiv", weight_max=1000)
    print(f"route(city='Kyiv', weight_max=1000) -> {[p.tracking for p in kyiv_light]}")
 
    try:
        route(unknown_field=1)
    except TypeError as exc:
        print(f"Невідомий критерій, перехоплено TypeError: {exc}")
    print()
 
    print("=== 4. Пошук за ідентифікатором у стилі EAFP (3.4) ===")
    found = route.get("UA-100003")
    print(f"route.get('UA-100003') -> {found}")
 
    try:
        route.get("ZZ-999999")
    except ParcelNotFound as exc:
        print(f"Відсутній ідентифікатор, перехоплено ParcelNotFound: {exc}")
 
 
def main() -> None:
    demo_weight()
    print()
    demo_parcel()
    print()
    demo_route()
 
 
if __name__ == "__main__":
    main()