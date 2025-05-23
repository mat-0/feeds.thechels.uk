# News

A repository to track third party (RSS) feeds from various insurance sites as GitHub issues. Note this is quite noisy.

## Adding a new feed

To add a new feed, update the relevant Python files in the repository:

1. **Locate the feed configuration**: Open the Python file (e.g., `feeds.py` or similar) where existing feeds are listed.
2. **Add your feed**: Insert a new entry with the feed's URL and any required metadata (such as name, tags, etc.) following the existing format.
3. **Save your changes**: Commit and push the updated Python file to the repository.
4. **Test the feed**: Run the script that processes the feeds to ensure your new feed is working correctly and is being tracked as expected.

## Example feed configuration

```python
URL_1 ="https://sub.domain.tld/feed/"

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()

        urls = [URL_1, ...]
        all_items = []
        ...

```
