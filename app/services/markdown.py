from app.schemas import ProjectCreate

def to_markdown_list(items:list[str]|None):
    if not items:
        return ""
    return "\n".join(f"- {item}" for item in items)

def create_project_markdown(project: ProjectCreate):
    markdown = f"""# {project.name}

## Overview

{project.overview}

## Technologies

{to_markdown_list(project.technologies)}

## Team

{to_markdown_list(project.team)}

## Features

{to_markdown_list(project.features)}
"""

    return markdown
