import hyperdiv as hd
from .page import page

router = hd.router()


@router.not_found
def not_found():
    with page() as p:
        p.title("# Not Found")
        hd.alert(
            "Oops, it doesn't look like there is anything here.",
            opened=True,
            variant="danger",
        )
