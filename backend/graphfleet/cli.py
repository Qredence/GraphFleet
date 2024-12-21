"""
GraphFleet CLI tool for managing GraphRAG projects.
"""

import os
import shutil
from pathlib import Path

import typer
from rich import print
from rich.console import Console
from rich.panel import Panel

from graphfleet.core import GraphFleet

app = typer.Typer(help="GraphFleet CLI - Manage your GraphRAG projects with ease")
console = Console()

def get_project_dir() -> Path:
    """Get project directory from environment or use default."""
    return Path(os.getenv("PROJECT_DIR", "./data"))

@app.command()
def init(
    project_dir: str = typer.Option(
        None,
        "--project-dir",
        "-d",
        help="Project directory (defaults to PROJECT_DIR env var)",
    )
):
    """Initialize a new GraphFleet project."""
    project_path = Path(project_dir) if project_dir else get_project_dir()
    
    try:
        # Create directory structure
        for subdir in ["raw", "processed", "indexes"]:
            (project_path / subdir).mkdir(parents=True, exist_ok=True)
            
        # Copy settings template
        template_path = Path(__file__).parent.parent / "templates" / "settings.yml"
        if template_path.exists():
            shutil.copy(template_path, project_path / "settings.yml")
        
        print(Panel.fit(
            "[green]Project initialized successfully![/green]\n"
            f"Project directory: {project_path}\n"
            "Directory structure created:\n"
            "  - raw/       (for input documents)\n"
            "  - processed/ (for intermediate files)\n"
            "  - indexes/   (for GraphRAG indexes)",
            title="GraphFleet Init"
        ))
    except Exception as e:
        print(f"[red]Error initializing project: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def index(
    project_dir: str = typer.Option(
        None,
        "--project-dir",
        "-d",
        help="Project directory (defaults to PROJECT_DIR env var)",
    )
):
    """Create index from documents in the raw directory."""
    project_path = Path(project_dir) if project_dir else get_project_dir()
    
    try:
        graph_fleet = GraphFleet(project_path)
        graph_fleet.create_index()
        
        print(Panel.fit(
            "[green]Index created successfully![/green]\n"
            f"Project directory: {project_path}\n"
            "Check the indexes/ directory for the results.",
            title="GraphFleet Index"
        ))
    except Exception as e:
        print(f"[red]Error creating index: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def autoprompt(
    project_dir: str = typer.Option(
        None,
        "--project-dir",
        "-d",
        help="Project directory (defaults to PROJECT_DIR env var)",
    )
):
    """Generate prompts automatically."""
    project_path = Path(project_dir) if project_dir else get_project_dir()
    
    try:
        graph_fleet = GraphFleet(project_path)
        graph_fleet.create_prompts()
        
        print(Panel.fit(
            "[green]Prompts generated successfully![/green]\n"
            f"Project directory: {project_path}",
            title="GraphFleet AutoPrompt"
        ))
    except Exception as e:
        print(f"[red]Error generating prompts: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host", "-h"),
    port: int = typer.Option(8000, "--port", "-p"),
    workers: int = typer.Option(1, "--workers", "-w"),
    reload: bool = typer.Option(True, "--reload/--no-reload"),
):
    """Start the GraphFleet API server."""
    import uvicorn
    
    print(Panel.fit(
        f"Starting GraphFleet API server\n"
        f"Host: {host}\n"
        f"Port: {port}\n"
        f"Workers: {workers}\n"
        f"Reload: {reload}",
        title="GraphFleet Server"
    ))
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        workers=workers,
        reload=reload,
    )

if __name__ == "__main__":
    app()
