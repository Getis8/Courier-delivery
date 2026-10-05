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
 
    def __repr__(self) -> str:
        return f"Route({self._parcels!r})"