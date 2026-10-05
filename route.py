from courier_delivery.entities import Parcel
 
ALLOWED_QUERY_CRITERIA = ("city", "weight_max")
 
 
class ParcelNotFound(Exception):
    """Підіймається Route.get(), коли посилки з таким tracking немає."""
 
    def __init__(self, entity_id: str) -> None:
        super().__init__(f"Посилку з трек-номером {entity_id!r} не знайдено")
        self.entity_id = entity_id
 
 
class Route:
    def __init__(self, parcels=()) -> None:
        self._parcels = list(parcels)
        self._index = {parcel.tracking: parcel for parcel in self._parcels}
 
    # -- протокол послідовності (3.1) ----------------------------------------
    def __len__(self) -> int:
        return len(self._parcels)
 
    def __getitem__(self, index):
        if isinstance(index, slice):
            # для зрізу повертаємо новий Route, а не звичайний list
            return Route(self._parcels[index])
        return self._parcels[index]
 
    def __contains__(self, item) -> bool:
        tracking = item.tracking if isinstance(item, Parcel) else item
        return tracking in self._index
 
    def __iter__(self):
        return iter(self._parcels)
 
    # -- посторінковий обхід (3.2) -------------------------------------------
    def pages(self, page_size: int) -> "RoutePageIterator":
        return RoutePageIterator(self, page_size)
 
    # -- запит через виклик екземпляра як функції (3.3) ----------------------
    def __call__(self, **criteria) -> "Route":
        unknown = set(criteria) - set(ALLOWED_QUERY_CRITERIA)
        if unknown:
            raise TypeError(
                f"Невідомі критерії запиту: {sorted(unknown)}. "
                f"Припустимі критерії: {list(ALLOWED_QUERY_CRITERIA)}"
            )
 
        result = self._parcels
        if "city" in criteria:
            city = criteria["city"]
            result = [p for p in result if p.dest_city == city]
        if "weight_max" in criteria:
            weight_max = criteria["weight_max"]
            result = [p for p in result if p.weight.grams <= weight_max]
        return Route(result)
 
    # -- пошук за ідентифікатором у стилі EAFP (3.4) --------------------------
    def get(self, entity_id: str) -> Parcel:
        try:
            return self._index[entity_id]
        except KeyError:
            raise ParcelNotFound(entity_id) from None
 
    # -- об'єднання колекцій (4.1) --------------------------------------------
    def __add__(self, other: "Route") -> "Route":
        if not isinstance(other, Route):
            return NotImplemented
        combined = list(self._parcels)
        seen_ids = set(self._index.keys())
        for parcel in other:
            if parcel.tracking not in seen_ids:
                combined.append(parcel)
                seen_ids.add(parcel.tracking)
        return Route(combined)
 
    def __radd__(self, other):
        # sum([route_a, route_b, route_c]) стартує з 0: 0 + route_a.
        # У цьому разі просто повертаємо копію поточної колекції.
        if other == 0:
            return Route(self._parcels)
        if isinstance(other, Route):
            return other.__add__(self)
        return NotImplemented
 
    def __repr__(self) -> str:
        return f"Route({self._parcels!r})"
 
 
class RoutePageIterator:
    """
    Ітератор посторінкового обходу Route. Не копіює елементи — тримає
    посилання на той самий Route і поточний індекс, звертаючись до його
    __len__ / __getitem__ при кожному __next__.
    """
 
    def __init__(self, route: Route, page_size: int) -> None:
        if page_size <= 0:
            raise ValueError("розмір сторінки повинен бути додатним")
        self._route = route
        self._page_size = page_size
        self._position = 0
 
    def __iter__(self) -> "RoutePageIterator":
        return self
 
    def __next__(self) -> list:
        if self._position >= len(self._route):
            raise StopIteration
        start = self._position
        end = min(start + self._page_size, len(self._route))
        page = [self._route[i] for i in range(start, end)]
        self._position = end
        return page