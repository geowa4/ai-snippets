"""Demonstrates a simple way to convert a PDF to Markdown using docling."""

from pathlib import Path

from docling.document_converter import DocumentConverter


def convert_pdf_to_markdown(pdf: Path) -> str:
    """Convert PDF to Markdown using docling."""
    converter = DocumentConverter()
    doc = converter.convert(pdf.absolute()).document
    return doc.export_to_markdown()


def main() -> None:
    """Print PDF as Markdown."""
    pdf = Path("sample.pdf")
    if not pdf.exists():
        return

    print(convert_pdf_to_markdown(pdf))


if __name__ == "__main__":
    main()
