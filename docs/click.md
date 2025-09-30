# Click

You can use Click to build simple command-line apps in Python.

```python
import click

@click.command()
@click.option('--name', prompt='Your name')
def hello(name):
    click.echo(f"Hello {name}!")

if __name__ == '__main__':
    hello()
```


Run with:

```
python app.py --name Jeremy
```

	•	@click.command() → marks function as CLI command
	•	@click.option() / @click.argument() → define inputs
	•	click.echo() → prints output

That’s it: decorate functions, add options/arguments, then run.
