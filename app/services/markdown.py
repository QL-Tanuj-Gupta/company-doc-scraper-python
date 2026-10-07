from app.schemas import ProjectCreate


def create_project_markdown(project: ProjectCreate):
    markdown = f"""# {project.name}

## Overview

{project.overview}

## Technologies

{project.technologies}

## Team

{project.team}

## Features

{project.features}
"""

    return markdown
