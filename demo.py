"""
demo.py

Демонстрація роботи об'єкта-значення Weight (завдання 1, пункт 1.6).

Запуск:
    python -m courier_delivery.demo
"""

from courier_delivery.value_objects import Weight, WeightDC


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


def main() -> None:
    demo_weight()


if __name__ == "__main__":
    main()
