from courier_delivery.entities import Parcel
 
 
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