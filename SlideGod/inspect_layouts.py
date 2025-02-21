from pptx import Presentation

# Replace with the path to your base template PPTX
prs = Presentation("base_template.pptx")

for i, layout in enumerate(prs.slide_layouts):
    print(i, layout.name)
