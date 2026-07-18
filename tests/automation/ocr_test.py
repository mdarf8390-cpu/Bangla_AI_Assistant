"""
=============================================
AYESHA AI

OCR TEST

Purpose
-------
Test OCR Engine

=============================================
"""

from automation.ocr_control import ocr


def main():

    print("=" * 50)
    print("AYESHA OCR TEST")
    print("=" * 50)

    print()

    print("OCR Available :",
          ocr.is_available())

    print(
        "Version :",
        ocr.get_version()
    )

    print()

    print("Reading Screen...")
    print("-" * 50)

    text = ocr.read_screen()

    if text:

        print(
            text[:500]
        )

    else:

        print(
            "No Text Found"
        )

    print()

    keyword = "Chrome"

    print(
        f"Searching : {keyword}"
    )

    found = ocr.find_text(
        keyword
    )

    print(
        "Found :",
        found
    )

    print()

    position = ocr.find_text_position(
        keyword
    )

    if position:

        print(
            "Position Found"
        )

        print(position)

    else:

        print(
            "Position Not Found"
        )

    print()

    print("=" * 50)
    print("OCR TEST COMPLETED")
    print("=" * 50)


if __name__ == "__main__":

    main()