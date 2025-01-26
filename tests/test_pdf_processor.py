from utils.pdf_processor import process_pdf

def test_process_pdf():
    file_path = "data/sample.pdf"
    retriever = process_pdf(file_path)
    assert retriever is not None
