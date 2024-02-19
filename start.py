import hyperdiv as hd
from hyperdiv_docs.main import main

index_page = hd.index_page(
    title="Hyperdiv Docs",
    description="Learn how to use the Hyperdiv web framework",
    keywords=("hyperdiv", "python", "web framework", "rapid development"),
    favicon="/assets/hd-logo-white.svg",
)


hd.run(main, index_page=index_page)
