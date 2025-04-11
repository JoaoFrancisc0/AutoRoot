from bs4 import BeautifulSoup

def add_quotes_to_columns(file_path, column_indices):
    try:
        # Try opening the file with UTF-8, fall back to UTF-16 if it fails
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="utf-16") as f:
                soup = BeautifulSoup(f, "html.parser")

        table = soup.find("table")
        if not table:
            # Attempt to find the table ignoring possible namespaces or attributes
            table = soup.find("table", attrs={"border": "1"})
        if not table:
            raise ValueError("No table found in the HTML.")

        # Iterate over all rows (<tr>) that contain cells (<td>)
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            for col_index in column_indices:
                if len(cells) > col_index:
                    cell = cells[col_index]
                    # Get the current content of the cell (removing extra spaces)
                    text = cell.get_text(strip=True)
                    # If the content is not already quoted, wrap it in quotes
                    if not (text.startswith('"') and text.endswith('"')):
                        cell.string = f'"{text}"'

        # Save the modified HTML with a new filename
        new_file_path = file_path.replace(".xls", "_c.xls")

        with open(new_file_path, "w", encoding="utf-16") as f:
            f.write(str(soup))

        return new_file_path
    except Exception as e:
        print(f"Error processing the file: {e}")
        raise
