import json
import requests
from bs4 import BeautifulSoup


def get_top_hf_papers(n: int):
    """
    Fetches the top N papers from the Hugging Face papers page based on the number of votes.
    """
    url = "https://huggingface.co/papers"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve papers: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    papers = soup.find_all("article")

    paper_info = []
    for paper in papers:
        title = paper.find("h3").text.strip() if paper.find("h3") else "No Title"
        link = paper.find("a")["href"] if paper.find("a") else "#"
        vote_info = paper.find(
            "div", {"class": "flex flex-wrap items-center gap-2.5 pt-1"}
        ).find("div", {"class": "leading-none"})
        thumbnail = paper.find("img")["src"] if paper.find("img") else ""
        author_list = paper.find(
            "ul", {"class": "flex items-center flex-row-reverse text-sm"}
        )

        authors = []
        if author_list:
            for author in author_list.find_all("li"):
                if author.has_attr("title"):
                    authors.append(author["title"])

        paper_info.append(
            {
                "title": title,
                "link": link,
                "votes": int(vote_info.text.strip())
                if vote_info and vote_info.text.strip().isdigit()
                else 0,
                "thumbnail": thumbnail,
                "authors": ", ".join(authors) if authors else "Unknown",
            }
        )

    paper_info.sort(key=lambda x: x["votes"], reverse=True)
    top_papers = paper_info[:n]

    for i, paper in enumerate(top_papers):
        paper_url = f"https://huggingface.co{paper['link']}"
        paper_response = requests.get(paper_url)
        if paper_response.status_code != 200:
            print(
                f"Failed to retrieve paper details for {paper['title']}: {paper_response.status_code}"
            )
            continue

        paper_soup = BeautifulSoup(paper_response.text, "html.parser")
        published_date_div = paper_soup.find(
            "div",
            {
                "class": "mb-6 flex flex-wrap gap-2 text-sm text-gray-500 max-sm:flex-col sm:items-center sm:text-base md:mb-8"
            },
        ).find("div")
        published_date_text = ""
        if published_date_div:
            published_date_text = published_date_div.text.split("Published on ")[
                1
            ].strip()

        abstract_div = paper_soup.find("div", {"class": "pb-8 pr-4 md:pr-16"}).find("p")
        abstract = (
            abstract_div.text.strip() if abstract_div else "No abstract available"
        )

        top_papers[i]["published_date"] = published_date_text
        top_papers[i]["abstract"] = abstract

    return json.dumps(top_papers, indent=2)


get_top_hf_papers_json = {
    "type": "function",
    "function": {
        "name": "get_top_hf_papers",
        "description": "Get the top N papers from the Hugging Face papers page based on the number of votes.",
        "parameters": {
            "type": "object",
            "properties": {
                "n": {
                    "type": "integer",
                    "description": "Number of top papers to fetch.",
                }
            },
            "required": ["n"],
        },
    },
}

if __name__ == "__main__":
    top_papers = get_top_hf_papers(5)
    for paper in top_papers:
        print(f"Title: {paper['title']}")
