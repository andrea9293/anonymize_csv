# CSV Anonymization Tool (Python with Faker and spaCy) - Anonymize All Columns

This Python tool anonymizes **all columns** of a CSV file, replacing sensitive data within every cell. It utilizes `faker` to generate fake data and `spaCy` for Named Entity Recognition (NER) to improve the accuracy of name anonymization in text-based columns. **Importantly, some anonymization techniques, particularly for IDs, rely on keyword-based regular expressions tailored to specific patterns.**

## Purpose

The main purpose is to perform broad anonymization of CSV data, replacing **all information** to protect privacy. This is useful for scenarios where you need to:

*   Share a completely anonymized version of a CSV, ensuring no original data is directly identifiable.
*   Create datasets for testing, development, or demonstration where all information should be fictitious.
*   Generate a CSV output where every column is replaced with fake, but plausibly structured, data.

**Important Note:** This tool is designed for *full* anonymization, processing every column.  It's crucial to understand that **data type awareness is not preserved**, and columns that are not text-based (e.g., numerical IDs, dates, categories) will also be processed and replaced.  Furthermore, **ID anonymization relies on specific keyword-based regular expressions and is not a generic ID detection system.** Review the output carefully to ensure it aligns with your anonymization goals and that the resulting data remains useful for your intended purpose. For more selective or data-type-aware anonymization, consider customizing the script or using previous versions of this tool.

## Prerequisites

Before using this tool, ensure you have the following installed:

1.  **Python:**  Python 3.x is required. [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **Faker Library:**  Generates fake data (names, companies, emails, phone numbers, etc.).

    ```bash
    pip install faker
    ```

3.  **spaCy Library:** For advanced Natural Language Processing, used for Named Entity Recognition to improve name anonymization in text columns.

    ```bash
    pip install spacy
    ```

4.  **Italian spaCy Language Model:** Required for Italian text processing.

    ```bash
    python -m spacy download it_core_news_lg  # Recommended for better accuracy (may be slower)
    ```
    or
    ```bash
    python -m spacy download it_core_news_sm  # Faster, potentially less accurate
    ```

## How to Use

1.  **Input CSV File (`input.csv`):**
    *   Place your semicolon (`;`) delimited CSV file as `input.csv` in the same directory as `anonymize_csv.py`.
    *   **All columns** of this CSV will be anonymized.

2.  **Run the Script:**
    *   Open your terminal, navigate to the script's directory.
    *   Execute:

        ```bash
        python anonymize_csv.py
        ```

3.  **Output CSV File (`output_anonymized.csv`):**
    *   The anonymized CSV, with all columns processed, will be saved as `output_anonymized.csv` in the same directory.

## Customization

While all columns are processed by default, customization is possible:

*   **Selective Column Exclusion:** Modify the main loop in the script to skip anonymization for specific column indices if needed.
*   **Adjust Anonymization Logic:**
    *   **Names/Companies:** Customize `anonymize_name()` and `anonymize_company()` for different fake data generation.
    *   **Emails/Phones/IDs:** Edit `anonymize_email()`, `anonymize_phone()`, `anonymize_id()`, and `anonymize_email_phone_ids()` to refine regexes or fake data.
    *   **Named Entity Recognition:** Experiment with spaCy models or entity labels in `anonymize_text_spacy()`.
*   **Data Type Specific Handling (Advanced):** Implement data type detection and apply different anonymization functions based on column type for more nuanced control.
*   **Customize Regular Expressions:** **Important:** The script relies on regular expressions to identify and anonymize specific IDs (Case IDs, Account IDs, Contract IDs, etc.). These regexes are currently tailored to match patterns and keywords like "case", "ac", "contratto", "SCTASK", "ODS", "BP-000", and numerical prefixes like "09", "20000", "350", etc., **which are specific to the provided example data.**

    **If your CSV data uses different keywords or ID formats, you will need to modify the regular expressions within the `anonymize_email_phone_ids()` function to correctly identify and anonymize IDs in your dataset.**

    For example, to adjust the Case ID regex if your Case IDs are formatted differently, you would modify lines like:

    ```python
    for case_id in set(re.findall(r'\b0?9\d{6,7}\b', text)): # Original Case ID regex
        text = text.replace(case_id, anonymize_id(case_id, case_id_mapping, 'CASE'))
    ```

    to match your specific Case ID pattern.  You can use online regex testers (like [https://regex101.com/](https://regex101.com/)) to help you create and test your regular expressions.

## Important Notes and Limitations

*   **Data Type Agnostic:** Anonymization is applied as text processing to all columns, without preserving original data types.
*   **Keyword-Based Regexes for IDs:** **ID anonymization is NOT generic.** It depends on regular expressions designed for specific keyword prefixes and numerical patterns observed in the example data. **Adapt these regexes if your ID formats are different.**
*   **Accuracy of NER:** spaCy improves name recognition but is not perfect. Review output.
*   **Performance:** spaCy NER is resource-intensive; large files may take longer.
*   **Potential Over-Anonymization:** Anonymizing all columns may reduce data utility. Consider selective anonymization if necessary.
*   **Review Output:**  Thoroughly check `output_anonymized.csv` to ensure correct and useful anonymization.
*   **No Perfect Anonymity Guarantee:**  Perfect anonymity is complex. This tool enhances privacy but may not eliminate all re-identification risks.

**Disclaimer:** This tool is provided as-is for informational and convenience purposes. Use it responsibly and verify that anonymization meets your specific needs and legal requirements, especially regarding the keyword-dependent nature of ID anonymization.