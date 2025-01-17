import pdfplumber
import pandas as pd
import csv
from io import StringIO
from openai import OpenAI

class SyllabusProcessor:
    def __init__(self):
        self.client = OpenAI()

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text

    def clean_response_content(self, response_content):
        if response_content.startswith("```csv"):
            response_content = response_content[6:]
        if response_content.endswith("```"):
            response_content = response_content[:-3]
        return response_content.strip()

    def query_openai_and_summarize(self, pdf_text):
        prompt = (
            """
            Based on the class I am taking, generate the programming language skills I have learned from class, like C#, HTML, Java, etc, and what my level for each skill(from 1-10, 10 is most skillful).
            Summarize the document into a structured CSV format. The title row should be "name", "skill, level".
            Write each skill for each row.
            Only the CSV content, no additional content.
            \n\n
            """
            + pdf_text
        )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_content = response.choices[0].message.content
        return self.clean_response_content(response_content)

    def save_summary_to_csv(self, summary):
        csv_reader = csv.reader(StringIO(summary), delimiter=',', quotechar='"')
        rows = list(csv_reader)

        max_columns = max(len(row) for row in rows)
        for row in rows:
            while len(row) < max_columns:
                row.append("")

        df = pd.DataFrame(rows[1:], columns=rows[0])
        # df.to_csv(output_csv_path, index=False)

        return df

    def summarize_pdf_to_csv(self, pdf_path):
        pdf_text = self.extract_text_from_pdf(pdf_path)
        summary = self.query_openai_and_summarize(pdf_text)
        return self.save_summary_to_csv(summary)
        # print(f"Summary saved to {output_csv_path}")

if __name__ == "__main__":
    summarizer = SyllabusProcessor()

    pdf_path = "test_1.pdf"
    output_csv_path = "summary.csv"

    summarizer.summarize_pdf_to_csv(pdf_path)