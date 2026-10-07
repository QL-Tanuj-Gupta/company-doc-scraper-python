import re

def parse_project_markdown(markdown:str):
  sections = {}

  pattern = r"## (.+?)\n\n(.*?)(?=\n## |\Z)"

  matches = re.findall(pattern,markdown,re.DOTALL)

  for title,content in matches:
    sections[title.strip().lower()] = content.strip()

  name_match = re.search(r"^# (.+)$",markdown,re.MULTILINE)

  name = name_match.group(1).strip() if name_match else""

  return{
    "name":name,
    "overview": sections.get("overview",""),
    "technologies": sections.get("technologies",""),
    "team": sections.get("team",""),
    "features": sections.get("features",""),
  }

