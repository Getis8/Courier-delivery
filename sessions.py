"""
sessions.py

Завдання 6. Контекстний менеджер пакетних змін.

DispatchSession — сеанс атомарних пакетних змін екземпляра Route
(наприклад, додавання кількох посилок одним "рейсом"). Усі зміни,
зроблені всередині блоку with, застосовуються разом лише за
відсутності винятку; якщо всередині блоку стався виняток — колекція
повертається рівно до того стану, який був на момент входу в блок,
а сам виняток не приховується і летить далі викликачу.

Приклад:
    route = Route()
    with DispatchSession(route) as session:
        session.add_parcel(tracking="UA-900001", weight=500,
                            dest_city="Kyiv", cost=50)
        session.add_parcel(tracking="UA-900002", weight=700,
                            dest_city="Lviv", cost=60)
        raise RuntimeError("щось пішло не так")
    # -> обидва add_parcel скасовані, len(route) те саме, що й до with,
    #    а RuntimeError долітає до місця виклику.
"""

import copy

from courier_delivery.route import Route


class DispatchSession:
    """Контекстний менеджер атомарного пакетного оновлення Route."""

    def __init__(self, route: Route) -> None:
        self._route = route
        self._snapshot = None

    def __enter__(self) -> Route:
        # Знімок стану на момент входу — повна незалежна копія,
        # яку в разі винятку підставимо назад замість поточного стану.
        self._snapshot = copy.deepcopy(self._route)
        return self._route

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            # Відкочуємо стан того самого об'єкта Route (а не підміняємо
            # посилання), щоб зовнішній код, який тримає цю змінну,
            # побачив саме відкочений стан.
            self._route._parcels = self._snapshot._parcels
            self._route._index = self._snapshot._index
        # False -> виняток НЕ приховується, летить далі викликачу.
        return False
