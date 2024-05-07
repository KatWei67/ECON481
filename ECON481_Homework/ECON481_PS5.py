### Exercise 0
def github() -> str:
    """
    Return github link to PS5 .
    """

    return "https://github.com/<user>/<repo>/blob/main/<filename.py>"

### Exercise 1
import requests
from bs4 import BeautifulSoup

def scrape_code(url: str) -> str:
    """
    This functin scrape Python code from the given URL of a lecture page.

    Args:
    url (str): URL of the webpage to scrape.

    Returns:
    str: A string containing all the Python code in the lecture formatted
    """
    try:
        # Access to the URL
        req_obj = requests.get(url)
        req_obj.raise_for_status()  # Check the request status

        # Make the html more nicely formatted and readable
        soup = BeautifulSoup(req_obj.text, 'html.parser')

        # Find all code elements within <pre><code> tags
        # filter for the 'python' class
        code_text = soup.find_all('pre', {'class': 'python'})
        python_code = []

        # Process each code text found
        for text in code_text:
            if text.code:  # Check if there is a <code> element within <pre>
                code = text.code.get_text()  # Get text within each <code> tag

                # Check and skip iPython magic commands (lines starting with %)
                filtered_code = '\n'.join(line for line in code.splitlines() if not line.strip().startswith('%'))

                # Add the filtered_code to the list
                python_code.append(filtered_code)

        # Join all the python code into a single string with newlines
        return '\n'.join(python_code)

    except requests.RequestException as e:
        return f"Error fetching page: {e}"
    except Exception as e:
        return f"Error processing page content: {e}"


# Example URL (replace with the actual URL)
# url = "https://lukashager.netlify.app/econ-481/01_intro_to_python"
# scraped_code = scrape_code(url)
# print(scraped_code)
