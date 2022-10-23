from genanki import Note, CLOZE_MODEL  # type: ignore


if __name__ == "__main__":
    note = Note(
        model=CLOZE_MODEL, fields=["{{c1::Rome}} is the capital of {{c2::Italy}}", ""]
    )

    print(note)
