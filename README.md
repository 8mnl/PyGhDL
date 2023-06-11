# PyGhDL 

is a (very) simple One-File-Python3-Script used to download separate folders inside existing GitHub repositories, based on [this script](https://gist.github.com/pdashford/2e4bcd4fc2343e2fd03efe4da17f577d?permalink_comment_id=4274705#gistcomment-4274705) from GitHub gist.

Very simple means:
- It's one purpose only - it downloads folders inside repos
- No tests
- No error checks
- (Almost) no usage checks

It's a one file script with a one line command and thus requires thinking along.

## Usage

Edit your [GitHub Token](https://github.com/settings/tokens) (required to bypass the request limit):

```python
token = "YOUR_TOKEN_HERE"
```

Install requirements.txt ([PyGithub](https://github.com/PyGithub/PyGithub)) - **Note:** PyGhDL uses `PyGithub 1.58.2` - Newer versions might differ in terms of API authentication

```bash
pip install -r requirements.txt
```

Run the script:

```bash
python pyghdl.py <LINK>
```

## Example

```
python pyghdl.py https://github.com/hakluke/how-to-exit-vim/tree/master/assets
```

## License

```
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
```