## pymakepublic

This is rather a tiny library that allows you to explicitly mark your public Python APIs with `@pub` rather than creating an `__all__` list and adding to or updating it whenever you change your public APIs.

This isn't necessarily [PEP 844](https://peps.python.org/pep-0844/), though it's the same idea. This library leaves classes and functions that are not explicitly marked with `@pub` alone (assuming they are supposedly private), and you may normally underscore them to indicate they are private APIs. Note that in Python you can still import those so-called private APIs, so this library doesn't make an exception on that.

```python
# m.py
from pymakepublic import pub

@pub
class Foo: ...

class Bar: ...

@pub
def bar(): ...

def do_something(): ...
```

```bash
>>> import m
>>> m.__all__
['Foo', 'bar']
```
This works the same as manually adding them to `__all__`. Hence if you use both `@pub` and `__all__` you get a `DoubleExportsError`.

### Why?

PEP 844's motivation isn't far off from mine. Also checkout [this StackOverflow comment](https://stackoverflow.com/questions/44834/what-does-all-mean-in-python#comment111940064_6413).

### Contributing

Issues and PRs are very welcome.

### LICENSE

MIT