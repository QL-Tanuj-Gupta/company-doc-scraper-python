def parse_project_markdown(markdown:str):
  lines= markdown.splitlines()

  project = {
    "name":"",
    "overview":"",
    "technologies":"",
    "team":"",
    "features":""
  }

  current_section = None

  for line in lines:
    if line.startswith("# "):
      project["name"] = line[2:].strip()
    
    elif line.startswith("## "):
      current_section = line[3:].strip().lower()

    elif current_section:
      project[current_section] += line + "\n"
    
  
  for key in project:
    project[key] = project[key].strip()
  
  return project


