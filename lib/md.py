class MardownFile: 

    def __init__(self): 
        self.content = []

    def __add_content(self,element):
        self.content.append(element)
        return element

    def add_title(self,element):
        return self.__add_content(f"# {element}")

    def add_section(self,element):
        return self.__add_content(f"## {element}")

    def add_subsection(self,element):
        return self.__add_content(f"### {element}")

    def add_element(self,element):
        return self.__add_content(f"{element}")

    def add_element_quote(self,element):
        return self.__add_content(f"```{element}```")

    def add_image(self,desc,url):
        return self.__add_content(f"![{desc}]({url})")

    def write(self,path_file):
        with open(path_file, "w") as text_file:
            text_file.write("\n".join(self.content))