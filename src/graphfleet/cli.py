import click
from .graphfleet import GraphFleet
from .config import settings
import json

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    ctx.obj['GF'] = GraphFleet()

@cli.command()
@click.pass_context
def info(ctx):
    """Display configuration information."""
    click.echo(f"Debug mode is {'on' if ctx.obj['DEBUG'] else 'off'}")
    click.echo(f"API Base: {settings.api_base}")
    click.echo(f"API Version: {settings.api_version}")
    click.echo(f"Deployment Name: {settings.deployment_name}")

@cli.command()
@click.argument('question')
@click.option('--method', default='global', type=click.Choice(['global', 'local']))
def query(question, method):
    """Query the knowledge graph."""
    gf = GraphFleet()
    answer, confidence = gf.query(question, method=method)
    click.echo(f"Answer: {answer}")
    click.echo(f"Confidence: {confidence}")

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def index(file_path):
    """Index documents from a JSON file."""
    with open(file_path, 'r') as f:
        documents = json.load(f)
    gf = GraphFleet()
    gf.index_documents(documents)
    click.echo(f"Indexed {len(documents)} documents.")

@cli.command()
def visualize():
    """Visualize the knowledge graph."""
    gf = GraphFleet()
    gf.visualize_graph()
    click.echo("Knowledge graph visualization saved as 'knowledge_graph.png'.")

@cli.command()
@click.argument('url')
@click.option('--output-format', default='text', type=click.Choice(['text', 'csv']))
def monthy_scrape(url, output_format):
    """Scrape a website using Monthy."""
    gf = GraphFleet()
    result = gf.monthy_scrape(url, output_format)
    click.echo(f"Scraped content:\n{result}")

if __name__ == "__main__":
    cli(obj={})