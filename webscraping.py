import requests
from bs4 import BeautifulSoup
import streamlit as st
from urllib.parse import urljoin
import pandas as pd

st.title("Website Scraper")

url = st.text_input("Enter any website URL:")

if st.button("Scrape"):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Title
        st.subheader("Title")
        st.write(soup.title.string.strip() if soup.title else "No title found")

        # Meta Description
        st.subheader("Meta Description")
        meta = soup.find("meta", attrs={"name":"description"})
        st.write(meta["content"].strip() if meta and meta.get("content") else "No meta description")

        # Headings (h1-h3)
        st.subheader("Headings")
        headings = [{"tag": f"h{level}", "text": tag.get_text(strip=True)}
                    for level in range(1, 4)
                    for tag in soup.find_all(f"h{level}")]
        st.dataframe(pd.DataFrame(headings) if headings else "No headings found")

        # Paragraphs (first 5)
        st.subheader("Paragraphs")
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        for i, ptxt in enumerate(paragraphs[:5], start=1):
            st.markdown(f"**Paragraph {i}:** {ptxt}") if paragraphs else st.write("No paragraphs found")

        # Links
        st.subheader("Links")
        links = [{"text": a.get_text(strip=True) or "No text", "url": urljoin(url, a["href"])}
                 for a in soup.find_all("a", href=True)]
        st.dataframe(pd.DataFrame(links) if links else "No links found")

    except Exception as e:
        st.error(f"Error: {e}")
