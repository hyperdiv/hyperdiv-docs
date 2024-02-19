# Docs Extractor

This module parses the hyperdiv repo and generates a JSON-encodable data structure that contains all the necessary metadata to render the docs components and prop type pages, without having to further reflect on hyperdiv code at runtime.

The JSON data structure can be statically generated and stored, so the code that extracts the docs metadata doesn't have to run until the file has to be re-generated.
