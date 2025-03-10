from .auth import router as auth_router
from .barcodes import router as barcodes_router
from .navigation import router as navigation_router
from .products import router as products_router
from .search import router as search_router
from .selection import router as selection_router
from .start import router as start_router


all_routers = [
    auth_router,
    barcodes_router,
    navigation_router,
    products_router,
    search_router,
    selection_router,
    start_router
]
